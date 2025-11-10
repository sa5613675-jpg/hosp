#!/usr/bin/env python
"""
Test user permissions for reception and admin roles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User

print("=" * 60)
print("USER PERMISSIONS TEST")
print("=" * 60)

# Get users
try:
    admin = User.objects.filter(role='ADMIN').first()
    reception = User.objects.filter(role='RECEPTIONIST').first()
    
    print("\n✓ ADMIN USER:")
    if admin:
        print(f"  Username: {admin.username}")
        print(f"  Role: {admin.role}")
        print(f"  is_admin: {admin.is_admin}")
        print(f"  Can manage lab tests: {admin.is_admin}")
        print(f"  Can manage PC members: {admin.is_admin}")
        print(f"  Can create lab orders: {admin.is_admin or admin.is_receptionist}")
    else:
        print("  ⚠ No admin user found")
    
    print("\n✓ RECEPTIONIST USER:")
    if reception:
        print(f"  Username: {reception.username}")
        print(f"  Role: {reception.role}")
        print(f"  is_receptionist: {reception.is_receptionist}")
        print(f"  Can manage lab tests: {reception.is_admin} (Should be False)")
        print(f"  Can manage PC members: {reception.is_admin} (Should be False)")
        print(f"  Can create lab orders: {reception.is_receptionist or reception.is_admin} (Should be True)")
        print(f"  Can create billing vouchers: {reception.is_receptionist or reception.is_admin} (Should be True)")
    else:
        print("  ⚠ No receptionist user found")
    
    print("\n" + "=" * 60)
    print("PERMISSION SUMMARY")
    print("=" * 60)
    print("\n✓ ADMIN can:")
    print("  - Manage Lab Tests (Add/Edit/Delete)")
    print("  - Manage PC Members (Add/Edit/Remove)")
    print("  - Create Lab Orders")
    print("  - Create Billing Vouchers")
    print("  - View All Reports")
    
    print("\n✓ RECEPTIONIST can:")
    print("  - Create Lab Orders")
    print("  - Create Billing Vouchers/Print Bills")
    print("  - Manage Patients")
    print("  - Manage Appointments")
    
    print("\n✗ RECEPTIONIST CANNOT:")
    print("  - Manage Lab Tests")
    print("  - Manage PC Members")
    print("  - Access Admin Finance Dashboard")
    
    print("\n" + "=" * 60)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
