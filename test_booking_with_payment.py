#!/usr/bin/env python
"""Test appointment booking with payment tracking"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from patients.models import Patient
from accounts.models import User
from appointments.models import Appointment
from finance.models import Income
from django.utils import timezone

# Get patients and doctors
patients = Patient.objects.all()[:5]
doctors = User.objects.filter(role='DOCTOR', is_active=True)
receptionist = User.objects.filter(role='RECEPTIONIST').first()

print("=" * 60)
print("APPOINTMENT BOOKING WITH PAYMENT TEST")
print("=" * 60)
print()

if not patients:
    print("❌ No patients found. Please register some patients first.")
elif not doctors:
    print("❌ No doctors found.")
elif not receptionist:
    print("❌ No receptionist found.")
else:
    print(f"✅ Found {patients.count()} patients")
    print(f"✅ Found {doctors.count()} doctors")
    print(f"✅ Receptionist: {receptionist.username}")
    print()
    
    print("Available Patients:")
    for p in patients:
        print(f"  - {p.get_full_name()} (ID: {p.patient_id}, Phone: {p.phone})")
    print()
    
    print("Available Doctors:")
    for d in doctors:
        print(f"  - Dr. {d.get_full_name()} ({d.specialization or 'General'})")
    print()
    
    # Check recent appointments
    today = timezone.now().date()
    recent_appointments = Appointment.objects.filter(appointment_date=today).count()
    recent_income = Income.objects.filter(date=today, source='CONSULTATION').count()
    
    print(f"Today's Appointments: {recent_appointments}")
    print(f"Today's Consultation Income Records: {recent_income}")
    print()
    
    if recent_income > 0:
        total_income = Income.objects.filter(date=today, source='CONSULTATION').aggregate(
            total=django.db.models.Sum('amount')
        )['total']
        print(f"💰 Total consultation income today: ৳{total_income}")
        print()
        
        print("Recent Income Records:")
        for inc in Income.objects.filter(date=today, source='CONSULTATION').order_by('-recorded_at')[:5]:
            print(f"  - {inc.income_number}: ৳{inc.amount} ({inc.payment_method})")
            print(f"    {inc.description}")
    
    print()
    print("✅ System ready for appointment booking!")
    print("   Login as: reception / 123456")
    print("   Go to: http://localhost:8000/appointments/create/")
