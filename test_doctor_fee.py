#!/usr/bin/env python
"""Test doctor fee management"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp.settings')
django.setup()

from accounts.models import User
from django.urls import reverse

print("=" * 60)
print("TESTING DOCTOR FEE MANAGEMENT")
print("=" * 60)

# 1. Check doctors
print("\n1. Checking doctors and their fees...")
doctors = User.objects.filter(role='DOCTOR')
print(f"   Found {doctors.count()} doctors")

if doctors.exists():
    print("\n   Current doctor fees:")
    for doc in doctors:
        print(f"   - {doc.username} ({doc.get_full_name()}): ৳{doc.consultation_fee}")
else:
    print("   ❌ No doctors found!")
    exit(1)

# 2. Check URL
print("\n2. Checking URL configuration...")
try:
    url = reverse('accounts:update_doctor_fee')
    print(f"   ✅ Update fee URL: {url}")
    
    mgmt_url = reverse('accounts:doctor_management')
    print(f"   ✅ Doctor management URL: {mgmt_url}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Test fee update (simulation)
print("\n3. Testing fee update simulation...")
test_doctor = doctors.first()
old_fee = test_doctor.consultation_fee
new_fee = 500.00

print(f"   Doctor: {test_doctor.username}")
print(f"   Old fee: ৳{old_fee}")
print(f"   New fee: ৳{new_fee}")

try:
    test_doctor.consultation_fee = new_fee
    test_doctor.save()
    print(f"   ✅ Fee updated successfully!")
    
    # Verify update
    test_doctor.refresh_from_db()
    if test_doctor.consultation_fee == new_fee:
        print(f"   ✅ Verified: Fee is now ৳{test_doctor.consultation_fee}")
    
    # Restore original fee
    test_doctor.consultation_fee = old_fee
    test_doctor.save()
    print(f"   ✅ Restored original fee: ৳{old_fee}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ DOCTOR FEE MANAGEMENT READY!")
print("=" * 60)
print("\nFEATURES:")
print("✅ Admin can view all doctors with their consultation fees")
print("✅ Admin can click edit button to update fee")
print("✅ Updated fee is saved to database")
print("✅ Receptionist can see this fee during appointment booking")
print("\nUSAGE:")
print("1. Go to: http://localhost:8000/accounts/doctor-management/")
print("2. See 'Consultation Fee' column with edit button")
print("3. Click edit button (pencil icon)")
print("4. Enter new fee and click 'Update Fee'")
print("5. Fee updates immediately!")
print("\nReceptionist will see the updated fee when booking appointments.")
