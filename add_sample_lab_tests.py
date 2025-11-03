#!/usr/bin/env python
"""Quick demo - Add sample lab tests via Django shell"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from lab.models import LabTest

print("=" * 70)
print("ADDING SAMPLE LAB TESTS")
print("=" * 70)
print()

# Sample lab tests to add
sample_tests = [
    {
        'test_code': 'HB001',
        'test_name': 'Hemoglobin (Hb)',
        'category': 'BLOOD',
        'description': 'Measures hemoglobin level in blood',
        'price': 80,
        'sample_type': 'Blood',
        'sample_volume': '2ml',
        'preparation_instructions': 'No special preparation needed',
        'turnaround_time': '2 hours',
    },
    {
        'test_code': 'THYROID01',
        'test_name': 'Thyroid Function Test (TSH, T3, T4)',
        'category': 'BIOCHEMISTRY',
        'description': 'Measures thyroid hormone levels',
        'price': 1200,
        'sample_type': 'Blood',
        'sample_volume': '5ml',
        'preparation_instructions': 'Morning sample preferred',
        'turnaround_time': '24 hours',
    },
    {
        'test_code': 'ECG01',
        'test_name': 'Electrocardiogram (ECG)',
        'category': 'OTHER',
        'description': 'Records electrical activity of the heart',
        'price': 300,
        'sample_type': 'N/A',
        'sample_volume': '',
        'preparation_instructions': 'Rest for 5 minutes before test',
        'turnaround_time': 'Immediate',
    },
]

print("Adding sample lab tests...")
print()

for test_data in sample_tests:
    test, created = LabTest.objects.get_or_create(
        test_code=test_data['test_code'],
        defaults=test_data
    )
    
    if created:
        print(f"✅ Added: {test.test_code} - {test.test_name} (৳{test.price})")
    else:
        print(f"ℹ️  Already exists: {test.test_code} - {test.test_name}")

print()
print("=" * 70)
print("CURRENT LAB TESTS")
print("=" * 70)
print()

all_tests = LabTest.objects.filter(is_active=True).order_by('category', 'test_name')
print(f"Total Active Tests: {all_tests.count()}")
print()

current_category = None
for test in all_tests:
    if test.category != current_category:
        current_category = test.category
        print(f"\n📁 {test.get_category_display()}")
        print("-" * 70)
    
    print(f"  {test.test_code:12} │ {test.test_name:40} │ ৳{test.price:>6}")

print()
print("=" * 70)
print("✅ Lab tests ready for use!")
print("=" * 70)
print()
print("To add more tests:")
print("1. Go to http://localhost:8000/admin/")
print("2. Login with admin credentials")
print("3. Click 'Lab tests' under LAB section")
print("4. Click 'Add Lab Test' button")
print()
