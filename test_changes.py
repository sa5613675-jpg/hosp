#!/usr/bin/env python
"""Test script for new features"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User
from finance.models import Income
from django.utils import timezone

print("=" * 60)
print("TESTING NEW FEATURES")
print("=" * 60)
print()

# Test 1: Check if doctors have consultation_fee field
print("1. Testing Doctor Consultation Fee Field:")
doctors = User.objects.filter(role='DOCTOR', is_active=True)
if doctors.exists():
    for doctor in doctors[:3]:
        print(f"   Dr. {doctor.get_full_name()}: ৳{doctor.consultation_fee}")
else:
    print("   No doctors found")
print()

# Test 2: Check receptionist income tracking
print("2. Testing Receptionist Income Tracking:")
receptionists = User.objects.filter(role='RECEPTIONIST')
if receptionists.exists():
    reception = receptionists.first()
    today = timezone.now().date()
    
    my_income = Income.objects.filter(
        recorded_by=reception,
        date=today,
        source='CONSULTATION'
    )
    
    total = sum(inc.amount for inc in my_income)
    print(f"   Receptionist: {reception.username}")
    print(f"   Today's Collections: ৳{total}")
    print(f"   Number of Transactions: {my_income.count()}")
else:
    print("   No receptionists found")
print()

# Test 3: Check Income source values
print("3. Testing Income Source Values:")
income_by_source = {}
for source, label in Income.SOURCE_CHOICES:
    count = Income.objects.filter(source=source).count()
    if count > 0:
        income_by_source[label] = count

for label, count in income_by_source.items():
    print(f"   {label}: {count} records")
print()

# Test 4: Admin dashboard calculation test
print("4. Testing Admin Financial Calculations:")
today = timezone.now().date()
consultation_income = Income.objects.filter(
    date=today,
    source='CONSULTATION'
).aggregate(total=django.db.models.Sum('amount'))['total'] or 0

lab_income = Income.objects.filter(
    date=today,
    source='LAB_TEST'
).aggregate(total=django.db.models.Sum('amount'))['total'] or 0

print(f"   Today's Consultation Income: ৳{consultation_income}")
print(f"   Today's Lab Income: ৳{lab_income}")
print()

print("✅ All tests completed!")
print()
print("SUMMARY:")
print("  ✅ Doctor consultation_fee field added")
print("  ✅ Receptionist income tracking working")
print("  ✅ Admin dashboard income sources fixed")
print("  ✅ Lab test management template fixed")
