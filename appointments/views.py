from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Max
from django.views.decorators.http import require_GET
from io import BytesIO
from gtts import gTTS
from .models import Appointment, Prescription, Medicine
from .forms import QuickAppointmentForm
from patients.models import Patient
from accounts.models import User

def public_booking(request):
    """Public appointment booking page (no login required)"""
    if request.method == 'POST':
        form = QuickAppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Split full name into first and last name
                full_name = form.cleaned_data['full_name']
                name_parts = full_name.strip().split(maxsplit=1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                # Calculate date_of_birth from age
                age = form.cleaned_data['age']
                today = timezone.now().date()
                year_of_birth = today.year - age
                date_of_birth = timezone.datetime(year_of_birth, 1, 1).date()
                
                # Get or create patient
                phone = form.cleaned_data['phone']
                patient, created = Patient.objects.get_or_create(
                    phone=phone,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'date_of_birth': date_of_birth,
                        'gender': form.cleaned_data['gender'],
                        'email': '',
                        'address': 'Walk-in Patient',
                        'city': '',
                        'emergency_contact_name': '',
                        'emergency_contact_phone': '',
                        'emergency_contact_relation': '',
                    }
                )
                
                # Update patient info if exists
                if not created:
                    patient.first_name = first_name
                    patient.last_name = last_name
                    patient.date_of_birth = date_of_birth
                    patient.gender = form.cleaned_data['gender']
                    patient.save()
                
                # Get doctor
                doctor = form.cleaned_data['doctor']
                
                # Get next serial number for today
                last_serial = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=today
                ).aggregate(Max('serial_number'))['serial_number__max']
                
                next_serial = (last_serial or 0) + 1
                
                # Generate appointment number
                appointment_number = f"APT-{today.strftime('%Y%m%d')}-{doctor.id}-{next_serial:03d}"
                
                # Create appointment
                appointment = Appointment.objects.create(
                    appointment_number=appointment_number,
                    patient=patient,
                    doctor=doctor,
                    serial_number=next_serial,
                    appointment_date=today,
                    status='waiting',
                    reason=form.cleaned_data.get('reason', ''),
                    created_by=None  # Public booking
                )
                
                messages.success(
                    request,
                    f'✅ সিরিয়াল নিশ্চিত করা হয়েছে! আপনার সিরিয়াল নম্বর: {next_serial}<br>'
                    f'Appointment confirmed! Your serial number: {next_serial}<br>'
                    f'ডাক্তার: {doctor.get_full_name()}<br>'
                    f'Phone: {phone}'
                )
                
                # Redirect to success or back to form
                return redirect('appointments:public_booking')
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'দয়া করে সকল তথ্য সঠিকভাবে পূরণ করুন / Please fill all fields correctly')
    else:
        form = QuickAppointmentForm()
    
    return render(request, 'appointments/public_booking.html', {'form': form})

@login_required
def appointment_list(request):
    """List all appointments"""
    appointments = Appointment.objects.all().select_related('patient', 'doctor').order_by('-appointment_date', 'serial_number')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    """Create new appointment - Receptionist booking with schedule time and serial"""
    from django.utils import timezone
    from django.db.models import Max
    from accounts.models import User
    
    if request.method == 'POST':
        form = QuickAppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment, patient = form.save(created_by=request.user)
                fee = form.cleaned_data['consultation_fee']
                payment_method = form.cleaned_data['payment_method']
                messages.success(
                    request, 
                    f'✅ Appointment booked! Serial #{appointment.serial_number} for {patient.get_full_name()} | Payment: ৳{fee} ({payment_method})'
                )
                return redirect('appointments:appointment_create')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = QuickAppointmentForm()
    
    # Get today's appointments grouped by doctor
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        appointment_date=today
    ).select_related('patient', 'doctor').order_by('doctor', 'serial_number')
    
    # Group by doctor
    appointments_by_doctor = {}
    for apt in appointments:
        doctor_name = apt.doctor.get_full_name()
        if doctor_name not in appointments_by_doctor:
            appointments_by_doctor[doctor_name] = []
        appointments_by_doctor[doctor_name].append(apt)
    
    # Get all active doctors with their consultation fees
    doctors = User.objects.filter(role='DOCTOR', is_active=True).values('id', 'consultation_fee')
    
    context = {
        'form': form,
        'today': today,
        'appointments_by_doctor': appointments_by_doctor,
        'doctors': doctors,
    }
    
    return render(request, 'appointments/receptionist_booking.html', context)

@login_required
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def call_patient(request, pk):
    """Call specific patient - updates status and broadcasts to display (Doctor-specific)"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Security check: Only the assigned doctor can call their patient
    if appointment.doctor != request.user and not request.user.is_admin:
        messages.error(request, '❌ You can only call your own patients!')
        return redirect('accounts:doctor_dashboard')
    
    # Update status
    appointment.status = 'in_consultation'
    appointment.called_time = timezone.now()
    appointment.save()
    
    # Broadcast to display monitors via WebSocket
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        broadcast_data = {
            'type': 'patient_called',
            'patient_name': appointment.patient.get_full_name(),
            'queue_number': appointment.serial_number,
            'serial_number': appointment.serial_number,
            'doctor_name': appointment.doctor.get_full_name(),
            'room_number': appointment.room_number or 'Consultation Room'
        }
        
        print(f"📡 Broadcasting to display_monitor:")
        print(f"   Patient: {broadcast_data['patient_name']}")
        print(f"   Serial: {broadcast_data['queue_number']}")
        print(f"   Doctor: {broadcast_data['doctor_name']}")
        print(f"   Room: {broadcast_data['room_number']}")
        
        async_to_sync(channel_layer.group_send)(
            'display_monitor',
            broadcast_data
        )
        
        print(f"✅ Broadcast sent successfully")
    except Exception as e:
        print(f"❌ WebSocket broadcast error: {e}")
        import traceback
        traceback.print_exc()
    
    # Return JSON for AJAX
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'success': True, 'message': 'Patient called'})
    
    messages.success(request, f'✅ Called patient {appointment.patient.get_full_name()} - Serial #{appointment.serial_number}')
    return redirect(request.META.get('HTTP_REFERER', 'accounts:doctor_dashboard'))

@login_required
def complete_appointment(request, pk):
    """Complete appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.complete()
    messages.success(request, 'Appointment completed!')
    return redirect('appointments:appointment_list')

@login_required
def queue_display(request):
    """Display patient queue"""
    from django.utils import timezone
    today = timezone.now().date()
    
    appointments = Appointment.objects.filter(
        appointment_date=today,
        status__in=['WAITING', 'CALLED', 'IN_PROGRESS']
    ).select_related('patient', 'doctor').order_by('serial_number')
    
    return render(request, 'appointments/queue_display.html', {'appointments': appointments})

def display_monitor(request):
    """Public display monitor - no login required"""
    return render(request, 'appointments/display_monitor.html')


@require_GET
def bengali_tts(request):
    """Generate Bengali speech audio for the given text using Google TTS."""
    text = request.GET.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'Missing text parameter'}, status=400)

    try:
        tts = gTTS(text=text, lang='bn', slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        response = HttpResponse(audio_fp.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename="announcement.mp3"'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Pragma'] = 'no-cache'
        return response
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@login_required
def prescription_create(request, appointment_id):
    """Create or edit prescription - Doctors can write comprehensive prescriptions"""
    from datetime import datetime
    
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Check if prescription already exists
    try:
        prescription = Prescription.objects.get(appointment=appointment)
        is_edit = True
    except Prescription.DoesNotExist:
        prescription = None
        is_edit = False
    
    # Only doctor or admin can write prescriptions
    if not (request.user.is_doctor or request.user.is_admin):
        messages.error(request, 'Only doctors can write prescriptions!')
        return redirect('appointments:appointment_detail', pk=appointment_id)
    
    if request.method == 'POST':
        # Get all form data
        chief_complaint = request.POST.get('chief_complaint', '').strip()
        history = request.POST.get('history', '').strip()
        blood_pressure = request.POST.get('blood_pressure', '').strip()
        pulse = request.POST.get('pulse', '').strip()
        temperature = request.POST.get('temperature', '').strip()
        weight = request.POST.get('weight', '').strip()
        on_examination = request.POST.get('on_examination', '').strip()
        diagnosis = request.POST.get('diagnosis', '').strip()
        investigation = request.POST.get('investigation', '').strip()
        advice = request.POST.get('advice', '').strip()
        follow_up_date = request.POST.get('follow_up_date', '').strip()
        
        # Get medicine data (multiple rows)
        medicine_names = request.POST.getlist('medicine_name[]')
        medicine_dosages = request.POST.getlist('dosage[]')
        medicine_frequencies = request.POST.getlist('frequency[]')
        medicine_durations = request.POST.getlist('duration[]')
        medicine_instructions = request.POST.getlist('medicine_instructions[]')
        
        # Check required diagnosis field
        if not diagnosis:
            messages.error(request, 'Diagnosis is required!')
            context = {
                'appointment': appointment,
                'prescription': prescription,
                'is_edit': is_edit,
            }
            return render(request, 'appointments/prescription_write.html', context)
        
        try:
            # Create or update prescription
            if prescription:
                # Update existing
                prescription.chief_complaint = chief_complaint
                prescription.history = history
                prescription.blood_pressure = blood_pressure
                prescription.pulse = pulse
                prescription.temperature = temperature
                prescription.weight = weight
                prescription.on_examination = on_examination
                prescription.diagnosis = diagnosis
                prescription.investigation = investigation
                prescription.advice = advice
                if follow_up_date:
                    prescription.follow_up_date = follow_up_date
            else:
                # Create new prescription
                prescription = Prescription(
                    appointment=appointment,
                    patient=appointment.patient,
                    doctor=request.user,
                    chief_complaint=chief_complaint,
                    history=history,
                    blood_pressure=blood_pressure,
                    pulse=pulse,
                    temperature=temperature,
                    weight=weight,
                    on_examination=on_examination,
                    diagnosis=diagnosis,
                    investigation=investigation,
                    advice=advice,
                )
                
                # Generate prescription number
                today = datetime.now()
                prefix = f"RX{today.strftime('%Y%m%d')}"
                last_prescription = Prescription.objects.filter(
                    prescription_number__startswith=prefix
                ).order_by('prescription_number').last()
                
                if last_prescription:
                    last_number = int(last_prescription.prescription_number[-4:])
                    new_number = last_number + 1
                else:
                    new_number = 1
                
                prescription.prescription_number = f"{prefix}{new_number:04d}"
                
                if follow_up_date:
                    prescription.follow_up_date = follow_up_date
            
            prescription.save()
            
            # Clear existing medicines if editing
            if is_edit:
                prescription.medicines.all().delete()
            
            # Save medicines
            for i in range(len(medicine_names)):
                if medicine_names[i].strip():  # Only save non-empty medicines
                    Medicine.objects.create(
                        prescription=prescription,
                        medicine_name=medicine_names[i].strip(),
                        dosage=medicine_dosages[i].strip() if i < len(medicine_dosages) else '',
                        frequency=medicine_frequencies[i].strip() if i < len(medicine_frequencies) else '',
                        duration=medicine_durations[i].strip() if i < len(medicine_durations) else '',
                        instructions=medicine_instructions[i].strip() if i < len(medicine_instructions) else '',
                    )
            
            # Check if "Send to Reception" button was clicked
            if 'send_to_reception' in request.POST:
                # Update appointment status
                appointment.status = 'COMPLETED'
                appointment.save()
                messages.success(request, f'✅ Prescription saved & sent to reception! Rx No: {prescription.prescription_number}')
                return redirect('accounts:doctor_dashboard')
            else:
                messages.success(request, f'✅ Prescription saved successfully! Rx No: {prescription.prescription_number}')
                return redirect('appointments:prescription_print', pk=prescription.pk)
                
        except Exception as e:
            messages.error(request, f'Error saving prescription: {str(e)}')
    
    # GET request - show form
    context = {
        'appointment': appointment,
        'prescription': prescription,
        'is_edit': is_edit,
    }
    return render(request, 'appointments/prescription_write.html', context)

@login_required
def prescription_detail(request, pk):
    """View prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'appointments/prescription_detail.html', {'prescription': prescription})

@login_required
def prescription_print(request, pk):
    """Print professional prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    
    # Mark as printed
    if not prescription.is_printed:
        prescription.is_printed = True
        prescription.printed_at = timezone.now()
        prescription.printed_by = request.user
        prescription.save()
    
    return render(request, 'appointments/prescription_print_professional.html', {'prescription': prescription})


@login_required
def doctor_appointments_by_date(request):
    """Show doctor's appointments for selected date - Simple serial history"""
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    # Get selected date from query param or default to today
    from datetime import datetime, date
    date_str = request.GET.get('date', '')
    
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Get all appointments for this doctor on selected date - ordered by serial number
    appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date=selected_date
    ).select_related('patient').prefetch_related('prescriptions').order_by('serial_number')
    
    # Simple appointment list with prescription info
    appointments_list = []
    for apt in appointments:
        prescription = apt.prescriptions.first() if apt.prescriptions.exists() else None
        appointments_list.append({
            'appointment': apt,
            'prescription': prescription,
        })
    
    context = {
        'selected_date': selected_date,
        'appointments': appointments_list,
        'total_patients': appointments.count(),
    }
    
    return render(request, 'appointments/doctor_appointments_list.html', context)


@login_required
def reception_prescriptions_list(request):
    """Reception view of all prescriptions for printing"""
    if request.user.role not in ['RECEPTIONIST', 'ADMIN']:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    from datetime import date, timedelta
    
    # Filter options
    date_filter = request.GET.get('date', '')
    doctor_id = request.GET.get('doctor', '')
    status_filter = request.GET.get('status', 'all')  # all, printed, unprinted
    
    # Base query - today's prescriptions by default
    prescriptions = Prescription.objects.select_related(
        'patient', 'doctor', 'appointment'
    ).prefetch_related('medicines')
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            prescriptions = prescriptions.filter(created_at__date=filter_date)
        except:
            prescriptions = prescriptions.filter(created_at__date=date.today())
    else:
        # Default: today
        prescriptions = prescriptions.filter(created_at__date=date.today())
    
    if doctor_id:
        prescriptions = prescriptions.filter(doctor_id=doctor_id)
    
    if status_filter == 'printed':
        prescriptions = prescriptions.filter(is_printed=True)
    elif status_filter == 'unprinted':
        prescriptions = prescriptions.filter(is_printed=False)
    
    prescriptions = prescriptions.order_by('-created_at')
    
    # Get doctors list for filter
    doctors = User.objects.filter(role='DOCTOR', is_active=True)
    
    context = {
        'prescriptions': prescriptions,
        'doctors': doctors,
        'selected_date': date_filter or date.today().strftime('%Y-%m-%d'),
        'selected_doctor': doctor_id,
        'selected_status': status_filter,
    }
    
    return render(request, 'appointments/reception_prescriptions_list.html', context)

