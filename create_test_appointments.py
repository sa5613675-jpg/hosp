#!/usr/bin/env python
"""
Create sample appointments for testing doctor dashboard
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.append('/workspaces/hosp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.utils import timezone
from appointments.models import Appointment, Prescription, Medicine
from patients.models import Patient
from accounts.models import User

def create_sample_data():
    """Create sample appointments for past, today, and future"""
    
    # Get or create doctor
    try:
        doctor = User.objects.filter(role='DOCTOR').first()
        if not doctor:
            print("❌ No doctor found. Please create a doctor user first.")
            return
        print(f"✅ Using doctor: {doctor.get_full_name()}")
    except Exception as e:
        print(f"❌ Error getting doctor: {e}")
        return
    
    today = timezone.now().date()
    
    # Sample patient data
    patients_data = [
        {'name': 'Md. Abdul Rahman', 'age': 45, 'gender': 'M', 'phone': '01712345678', 'reason': 'জ্বর এবং মাথাব্যথা'},
        {'name': 'Fatima Begum', 'age': 35, 'gender': 'F', 'phone': '01812345679', 'reason': 'পেটে ব্যথা'},
        {'name': 'Karim Uddin', 'age': 60, 'gender': 'M', 'phone': '01912345680', 'reason': 'Diabetes check-up'},
        {'name': 'Amina Khatun', 'age': 28, 'gender': 'F', 'phone': '01612345681', 'reason': 'Cold and cough'},
        {'name': 'Habibur Rahman', 'age': 52, 'gender': 'M', 'phone': '01712345682', 'reason': 'Blood pressure'},
        {'name': 'Nasrin Akter', 'age': 38, 'gender': 'F', 'phone': '01812345683', 'reason': 'Headache'},
        {'name': 'Rafiq Ahmed', 'age': 48, 'gender': 'M', 'phone': '01912345684', 'reason': 'Back pain'},
        {'name': 'Sultana Begum', 'age': 42, 'gender': 'F', 'phone': '01612345685', 'reason': 'Stomach pain'},
    ]
    
    # Dates to create appointments
    dates = [
        today - timedelta(days=3),  # 3 days ago
        today - timedelta(days=1),  # Yesterday
        today,                       # Today
        today + timedelta(days=1),  # Tomorrow
        today + timedelta(days=2),  # Day after tomorrow
    ]
    
    print("\n📅 Creating appointments...")
    
    appointment_count = 0
    prescription_count = 0
    
    for date_obj in dates:
        date_str = date_obj.strftime('%Y-%m-%d')
        is_past = date_obj < today
        is_today = date_obj == today
        
        # Create 3-5 patients per day
        num_patients = 5 if is_today else 3
        
        for i in range(num_patients):
            patient_info = patients_data[i % len(patients_data)]
            
            # Get or create patient
            phone = patient_info['phone']
            patient, created = Patient.objects.get_or_create(
                phone=phone,
                defaults={
                    'first_name': patient_info['name'].split()[0],
                    'last_name': ' '.join(patient_info['name'].split()[1:]),
                    'date_of_birth': today - timedelta(days=patient_info['age']*365),
                    'gender': patient_info['gender'],
                    'address': 'Nazipur, Pirojpur',
                    'city': 'Pirojpur',
                }
            )
            
            # Create appointment
            serial = i + 1
            appointment, apt_created = Appointment.objects.get_or_create(
                doctor=doctor,
                patient=patient,
                appointment_date=date_obj,
                serial_number=serial,
                defaults={
                    'status': 'completed' if is_past else ('waiting' if is_today else 'waiting'),
                    'reason': patient_info['reason'],
                    'consultation_fee': 500,
                    'payment_status': 'paid' if is_past else 'unpaid',
                    'appointment_type': 'walk_in',
                }
            )
            
            if apt_created:
                appointment_count += 1
                print(f"  ✅ {date_str} - Serial #{serial}: {patient_info['name']}")
                
                # Add prescription for past appointments
                if is_past or (is_today and i < 2):
                    try:
                        prescription = Prescription.objects.create(
                            appointment=appointment,
                            patient=patient,
                            doctor=doctor,
                            chief_complaint=patient_info['reason'],
                            history='H/O present illness',
                            blood_pressure='120/80 mm Hg',
                            pulse='72/min',
                            on_examination='NAD',
                            diagnosis='General illness',
                            advice='বিশ্রাম নিন, বেশি পানি পান করুন'
                        )
                        
                        # Add medicines
                        Medicine.objects.create(
                            prescription=prescription,
                            medicine_name='Tab. Napa 500mg',
                            dosage='500mg',
                            frequency='1+0+1',
                            duration='5 days',
                            instructions='খাবারের পরে'
                        )
                        
                        Medicine.objects.create(
                            prescription=prescription,
                            medicine_name='Cap. Omeprazole 20mg',
                            dosage='20mg',
                            frequency='1+0+0',
                            duration='7 days',
                            instructions='সকালে খালি পেটে'
                        )
                        
                        prescription_count += 1
                        print(f"     📝 Prescription added: {prescription.prescription_number}")
                        
                    except Exception as e:
                        print(f"     ⚠️ Prescription error: {e}")
            else:
                print(f"  ⏭️  {date_str} - Serial #{serial}: Already exists")
    
    print(f"\n✅ Summary:")
    print(f"   Appointments created: {appointment_count}")
    print(f"   Prescriptions created: {prescription_count}")
    print(f"\n🎯 Test URLs:")
    print(f"   Doctor Dashboard: http://localhost:8000/accounts/dashboard/")
    print(f"   Display Monitor: http://localhost:8000/appointments/monitor/")

if __name__ == '__main__':
    create_sample_data()
