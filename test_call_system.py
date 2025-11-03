#!/usr/bin/env python
"""
Test script to manually trigger a patient call
Run: python test_call_system.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.utils import timezone
from appointments.models import Appointment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

print("="*60)
print("PATIENT CALL SYSTEM TEST")
print("="*60)

# Get or create a test appointment
today = timezone.now().date()
appointments = Appointment.objects.filter(
    appointment_date=today,
    status='waiting'
).first()

if not appointments:
    print("\n❌ No waiting appointments found for today")
    print("Please book an appointment first using the public booking page:")
    print("http://localhost:8000/appointments/book/")
    exit(1)

print(f"\n✅ Found waiting appointment:")
print(f"   Patient: {appointments.patient.get_full_name()}")
print(f"   Serial: {appointments.serial_number}")
print(f"   Doctor: {appointments.doctor.get_full_name()}")
print(f"   Room: {appointments.room_number or 'Consultation Room'}")

# Update status
appointments.status = 'in_consultation'
appointments.called_time = timezone.now()
appointments.save()

print(f"\n📡 Broadcasting to display monitors...")

# Broadcast to display monitors
try:
    channel_layer = get_channel_layer()
    
    broadcast_data = {
        'type': 'patient_called',
        'patient_name': appointments.patient.get_full_name(),
        'queue_number': appointments.serial_number,
        'serial_number': appointments.serial_number,
        'doctor_name': appointments.doctor.get_full_name(),
        'room_number': appointments.room_number or 'Consultation Room'
    }
    
    print(f"\n📦 Broadcast Data:")
    for key, value in broadcast_data.items():
        print(f"   {key}: {value}")
    
    async_to_sync(channel_layer.group_send)(
        'display_monitor',
        broadcast_data
    )
    
    print(f"\n✅ Broadcast sent successfully to 'display_monitor' group!")
    print(f"\n🎯 Check the display monitor page:")
    print(f"   http://localhost:8000/appointments/monitor/")
    print(f"\nThe patient should appear on the display with Bengali audio announcement!")
    
except Exception as e:
    print(f"\n❌ Error broadcasting: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
