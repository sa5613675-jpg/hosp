#!/usr/bin/env python
"""
Test script for serial booking workflow
Run: python manage.py shell < test_serial_workflow.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from patients.models import Patient
from appointments.models import Appointment
from datetime import date

print("\n" + "="*60)
print("TESTING SERIAL BOOKING WORKFLOW")
print("="*60 + "\n")

# Step 1: Get or create a doctor
print("Step 1: Getting doctor...")
doctor = User.objects.filter(role='DOCTOR', is_active=True).first()
if not doctor:
    print("❌ No doctor found! Please create doctors first.")
    exit(1)
print(f"✅ Using doctor: Dr. {doctor.get_full_name()}")

# Step 2: Get or create a test patient
print("\nStep 2: Creating test patient...")
patient, created = Patient.objects.get_or_create(
    phone='01700000001',
    defaults={
        'first_name': 'Test',
        'last_name': 'Patient',
        'date_of_birth': date(1990, 1, 1),
        'gender': 'M',
        'email': 'test@example.com',
        'address': 'Test Address'
    }
)
if created:
    print(f"✅ Created new patient: {patient.get_full_name()}")
else:
    print(f"✅ Using existing patient: {patient.get_full_name()}")

# Step 3: Create appointment with auto-serial
print("\nStep 3: Creating appointment (auto-serial)...")
today = timezone.now().date()

# Get next serial number
last_serial = Appointment.objects.filter(
    doctor=doctor,
    appointment_date=today
).aggregate(max_serial=django.db.models.Max('serial_number'))['max_serial']
next_serial = (last_serial or 0) + 1

appointment = Appointment.objects.create(
    patient=patient,
    doctor=doctor,
    appointment_date=today,
    appointment_time=timezone.now().time(),
    serial_number=next_serial,
    status='waiting',
    reason='Test appointment',
    room_number='Room 1'
)
print(f"✅ Created appointment: Serial #{appointment.serial_number}")
print(f"   - Patient: {appointment.patient.get_full_name()}")
print(f"   - Doctor: Dr. {appointment.doctor.get_full_name()}")
print(f"   - Status: {appointment.status}")
print(f"   - Schedule Time: {appointment.appointment_time}")

# Step 4: Simulate calling the patient
print("\nStep 4: Calling patient (simulating doctor action)...")
appointment.status = 'in_consultation'
appointment.called_time = timezone.now()
appointment.save()
print(f"✅ Patient called!")
print(f"   - New Status: {appointment.status}")
print(f"   - Called Time: {appointment.called_time}")

# Step 5: Check today's queue
print("\nStep 5: Today's Queue Summary:")
print("-" * 60)
today_appointments = Appointment.objects.filter(
    appointment_date=today,
    doctor=doctor
).order_by('serial_number')

print(f"Total appointments for Dr. {doctor.get_full_name()}: {today_appointments.count()}")
print("\nQueue List:")
for apt in today_appointments:
    status_icon = {
        'waiting': '⏳',
        'in_consultation': '👨‍⚕️',
        'completed': '✅',
        'cancelled': '❌'
    }.get(apt.status, '❓')
    
    print(f"  Serial #{apt.serial_number} - {apt.patient.get_full_name()} "
          f"[{status_icon} {apt.status.upper()}]")

# Step 6: Display Monitor Info
print("\n" + "="*60)
print("DISPLAY MONITOR INFO")
print("="*60)
print("\nTo view the display monitor:")
print("  URL: http://localhost:8000/appointments/monitor/")
print("\nThis page will:")
print("  ✅ Show when doctors call patients")
print("  ✅ Announce patient name in Bengali using TTS")
print("  ✅ Show serial number and room")
print("  ✅ Auto-hide after 15 seconds")
print("\nTest the audio by pressing 'T' on the display page!")

# Step 7: Access URLs
print("\n" + "="*60)
print("SYSTEM URLS")
print("="*60)
print("\n📋 Receptionist:")
print("   - Book Appointment: http://localhost:8000/appointments/create/")
print("   - Dashboard: http://localhost:8000/accounts/receptionist-dashboard/")

print("\n👨‍⚕️ Doctor:")
print(f"   - Dashboard: http://localhost:8000/accounts/doctor-dashboard/")
print("   - Queue: http://localhost:8000/appointments/queue/")

print("\n📺 Display Monitor (Public):")
print("   - Monitor: http://localhost:8000/appointments/monitor/")

print("\n" + "="*60)
print("✅ WORKFLOW TEST COMPLETE!")
print("="*60 + "\n")

print("\nNext Steps:")
print("1. Login as receptionist and book appointments at /appointments/create/")
print("2. Login as doctor and use 'Call Next' button")
print("3. Open display monitor in another browser/tab to see announcements")
print("\nCredentials (from LOGIN_QUICK_CARD.txt):")
print("  Admin: 01332856000 / 856000")
print("  Receptionists: 01332856002 / 856002")
