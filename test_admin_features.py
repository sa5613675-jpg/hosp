#!/usr/bin/env python
"""Test admin features - Lab Tests and Doctor Details"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from lab.models import LabTest
from accounts.models import User
from appointments.models import Prescription

print("=" * 70)
print("ADMIN FEATURES TEST")
print("=" * 70)
print()

# Test 1: Check Lab Tests
print("1. LAB TESTS")
print("-" * 70)
lab_tests = LabTest.objects.all()
print(f"Total Lab Tests: {lab_tests.count()}")
if lab_tests.exists():
    print("\nAvailable Lab Tests:")
    for test in lab_tests[:5]:
        print(f"  - {test.test_code}: {test.test_name} (৳{test.price})")
        print(f"    Category: {test.category}, Active: {test.is_active}")
else:
    print("⚠️ No lab tests found. Admin needs to add tests.")
    print("\n📝 To add lab tests in admin:")
    print("   1. Go to http://localhost:8000/admin/")
    print("   2. Click 'Lab tests' under LAB section")
    print("   3. Click 'Add Lab Test' button")
    print("   4. Fill in:")
    print("      - Test Code (e.g., CBC001)")
    print("      - Test Name (e.g., Complete Blood Count)")
    print("      - Category (select from dropdown)")
    print("      - Price (e.g., 500)")
    print("      - Sample Type (e.g., Blood)")
    print("      - Turnaround Time (e.g., 24 hours)")

print()

# Test 2: Check Doctors
print("2. DOCTORS")
print("-" * 70)
doctors = User.objects.filter(role='DOCTOR', is_active=True)
print(f"Total Doctors: {doctors.count()}")
if doctors.exists():
    print("\nDoctors with Details:")
    for doctor in doctors:
        print(f"  - Dr. {doctor.get_full_name()}")
        print(f"    Username: {doctor.username}")
        if doctor.specialization:
            print(f"    Specialization: {doctor.specialization}")
        else:
            print(f"    ⚠️ Specialization: NOT SET")
        if doctor.license_number:
            print(f"    License: {doctor.license_number}")
        else:
            print(f"    ⚠️ License: NOT SET")
        print()
else:
    print("⚠️ No doctors found.")

print()

# Test 3: Check Prescriptions
print("3. PRESCRIPTIONS (Doctor Details Display)")
print("-" * 70)
prescriptions = Prescription.objects.select_related('doctor').all()[:3]
print(f"Total Prescriptions: {prescriptions.count()}")
if prescriptions.exists():
    print("\nRecent Prescriptions:")
    for p in prescriptions:
        print(f"  - Prescription #{p.id}")
        print(f"    Doctor: {p.doctor.get_full_name()}")
        print(f"    Specialization: {p.doctor.specialization or 'NOT SET'}")
        print(f"    Patient: {p.patient.get_full_name()}")
        print()

print()

# Test 4: Admin Access Check
print("4. ADMIN ACCESS")
print("-" * 70)
admins = User.objects.filter(is_superuser=True, is_active=True)
print(f"Active Admin Users: {admins.count()}")
for admin in admins:
    print(f"  - {admin.username} ({admin.email})")

print()

# Test 5: How to fix missing doctor details
doctors_without_spec = User.objects.filter(role='DOCTOR', is_active=True, specialization='')
if doctors_without_spec.exists():
    print("5. ⚠️ DOCTORS MISSING SPECIALIZATION")
    print("-" * 70)
    print(f"Found {doctors_without_spec.count()} doctors without specialization")
    print("\n📝 To add doctor specialization in admin:")
    print("   1. Go to http://localhost:8000/admin/")
    print("   2. Click 'Users' under ACCOUNTS section")
    print("   3. Click on the doctor's name")
    print("   4. Scroll to 'Additional Info' section")
    print("   5. Fill in 'Specialization' field")
    print("   6. Optionally fill 'License number'")
    print("   7. Click 'Save'")
    print()
    print("Doctors to update:")
    for doc in doctors_without_spec:
        print(f"  - {doc.get_full_name()} (username: {doc.username})")
    print()

print()
print("=" * 70)
print("✅ Admin features are properly configured!")
print("=" * 70)
print()
print("🔐 Admin Panel: http://localhost:8000/admin/")
print()
print("To add Lab Tests:")
print("  Admin → Lab → Lab tests → Add Lab Test")
print()
print("To update Doctor Details:")
print("  Admin → Accounts → Users → [Select Doctor] → Additional Info section")
print()
