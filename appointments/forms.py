from django import forms
from .models import Appointment, Prescription, Medicine, DoctorSchedule, DoctorAvailability
from patients.models import Patient
from accounts.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta


class DoctorScheduleForm(forms.ModelForm):
    """Form for managing doctor schedules"""
    
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'day_of_week', 'start_time', 'end_time', 'max_patients', 
                  'consultation_duration', 'room_number', 'is_active']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_patients': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DoctorAvailabilityForm(forms.ModelForm):
    """Form for specific date availability"""
    
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'start_time', 'end_time', 'max_patients', 
                  'is_available', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_patients': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuickAppointmentForm(forms.Form):
    """Simple appointment booking form - creates patient and appointment with payment"""
    
    # Patient basic info
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter full name',
            'required': True
        }),
        label='Full Name'
    )
    
    age = forms.IntegerField(
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter age',
            'required': True
        }),
        label='Age'
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter phone number',
            'required': True
        }),
        label='Phone Number'
    )
    
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg'
        }),
        label='Gender'
    )
    
    # Doctor selection
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='DOCTOR', is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'doctor-select',
            'onchange': 'loadDoctorSchedule(this.value)'
        }),
        label='Select Doctor',
        empty_label='-- Choose a Doctor --'
    )
    
    # Optional reason
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Brief reason for visit (optional)',
            'rows': 3
        }),
        label='Reason for Visit'
    )
    
    # Payment fields
    consultation_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=300.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '300.00',
            'step': '0.01',
            'required': True
        }),
        label='Consultation Fee (৳)'
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('CASH', 'Cash'),
            ('BKASH', 'bKash'),
            ('NAGAD', 'Nagad'),
            ('ROCKET', 'Rocket'),
            ('CARD', 'Card'),
            ('BANK', 'Bank Transfer')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg'
        }),
        label='Payment Method'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom display for doctors
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.get_full_name()} - {obj.specialization or 'General'}"
    
    def save(self, created_by=None):
        """Create or get patient and create appointment with payment tracking"""
        from finance.models import Income
        from django.utils import timezone
        from django.db.models import Max
        from datetime import date
        
        full_name = self.cleaned_data['full_name']
        phone = self.cleaned_data['phone']
        age = self.cleaned_data['age']
        gender = self.cleaned_data['gender']
        doctor = self.cleaned_data['doctor']
        reason = self.cleaned_data.get('reason', '')
        consultation_fee = self.cleaned_data['consultation_fee']
        payment_method = self.cleaned_data['payment_method']
        
        # Split name into first and last
        name_parts = full_name.strip().split(maxsplit=1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Calculate approximate date of birth from age
        today = date.today()
        year_of_birth = today.year - age
        date_of_birth = date(year_of_birth, 1, 1)
        
        # Check if patient exists by phone AND name
        patient = Patient.objects.filter(
            phone=phone,
            first_name__iexact=first_name,
            last_name__iexact=last_name
        ).first()
        
        if not patient:
            # Create new patient
            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                phone=phone,
                email='',
                address='Walk-in Patient',
                city='',
                emergency_contact_name='',
                emergency_contact_phone='',
                emergency_contact_relation='',
                registered_by=created_by
            )
        
        # Get today's date
        today = timezone.now().date()
        
        # Get next serial number for today and this doctor
        last_serial = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).aggregate(Max('serial_number'))['serial_number__max'] or 0
        
        next_serial = last_serial + 1
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=today,
            appointment_time=timezone.now().time(),
            serial_number=next_serial,
            reason=reason,
            status='WAITING',
            created_by=created_by
        )
        
        # Record payment as income
        Income.objects.create(
            date=today,
            source='CONSULTATION',
            amount=consultation_fee,
            payment_method=payment_method,
            description=f'Consultation fee - Dr. {doctor.get_full_name()} - Patient: {patient.get_full_name()} (Serial #{appointment.serial_number})',
            recorded_by=created_by
        )
        
        return appointment, patient


class AppointmentForm(forms.ModelForm):
    """Form for creating appointments (traditional)"""
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Patient"
    )
    
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='DOCTOR'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Doctor"
    )
    
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'room_number', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Room 101'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special notes...'}),
        }


class PrescriptionForm(forms.ModelForm):
    """Form for writing prescriptions"""
    
    class Meta:
        model = Prescription
        fields = ['diagnosis', 'chief_complaint', 'advice', 'follow_up_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter diagnosis...'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Patient complaints...'}),
            'advice': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Advice to patient...'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MedicineForm(forms.ModelForm):
    """Form for adding medicines to prescription"""
    
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Twice daily'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 days'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# Formset for multiple medicines
from django.forms import inlineformset_factory

MedicineFormSet = inlineformset_factory(
    Prescription, 
    Medicine,
    form=MedicineForm,
    extra=5,
    can_delete=True,
    min_num=1,
    validate_min=True
)
