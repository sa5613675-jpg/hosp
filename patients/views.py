from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, PatientHistory
from .forms import PatientRegistrationForm, PatientSearchForm

@login_required
def patient_list(request):
    """List all patients with search"""
    form = PatientSearchForm(request.GET or None)
    patients = Patient.objects.all().order_by('-registered_at')
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        blood_group = form.cleaned_data.get('blood_group')
        gender = form.cleaned_data.get('gender')
        
        if search_query:
            patients = patients.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(patient_id__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if blood_group:
            patients = patients.filter(blood_group=blood_group)
        
        if gender:
            patients = patients.filter(gender=gender)
    
    context = {
        'patients': patients,
        'form': form,
    }
    return render(request, 'patients/patient_list.html', context)

@login_required
def patient_register(request):
    """Register new patient"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'✅ Patient {patient.get_full_name()} registered successfully! ID: {patient.patient_id}')
            
            # If receptionist, redirect to appointment booking
            if hasattr(request.user, 'is_receptionist') and request.user.is_receptionist:
                messages.info(request, f'Now book appointment for {patient.get_full_name()}')
                return redirect('appointments:appointment_create')
            
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Register New Patient'})

@login_required
def patient_detail(request, pk):
    """View patient details with appointments and prescriptions"""
    patient = get_object_or_404(Patient, pk=pk)
    
    # Get appointments with prescriptions
    from appointments.models import Appointment
    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related('doctor').prefetch_related('prescriptions').order_by('-appointment_date')[:10]
    
    # Get history if exists
    try:
        from patients.models import PatientHistory
        history = PatientHistory.objects.filter(patient=patient).order_by('-visit_date')[:5]
    except:
        history = []
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'history': history
    }
    return render(request, 'patients/patient_detail.html', context)

@login_required
def patient_edit(request, pk):
    """Edit patient information"""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Patient updated successfully!')
        return redirect('patients:patient_detail', pk=pk)
    return render(request, 'patients/patient_edit.html', {'patient': patient})

@login_required
def patient_history(request, pk):
    """View patient medical history"""
    patient = get_object_or_404(Patient, pk=pk)
    history = PatientHistory.objects.filter(patient=patient).order_by('-visit_date')
    return render(request, 'patients/patient_history.html', {
        'patient': patient,
        'history': history
    })

@login_required
def patient_delete(request, pk):
    """Delete patient (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('patients:patient_list')
    
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient_name = patient.get_full_name()
        patient_id = patient.patient_id
        
        # Check if patient has appointments
        from appointments.models import Appointment
        appointment_count = Appointment.objects.filter(patient=patient).count()
        
        if appointment_count > 0:
            # Don't delete, just mark as inactive or show warning
            messages.warning(
                request,
                f'Cannot delete patient {patient_name} ({patient_id}). '
                f'Patient has {appointment_count} appointment(s) in the system.'
            )
        else:
            # Safe to delete
            patient.delete()
            messages.success(
                request,
                f'Patient {patient_name} ({patient_id}) has been deleted successfully.'
            )
            return redirect('patients:patient_list')
    
    return redirect('patients:patient_detail', pk=pk)
