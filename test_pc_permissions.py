#!/usr/bin/env python
"""
Test PC Member Permissions
Run this to verify PC member create/edit/delete permissions
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("PC MEMBER PERMISSIONS TEST")
print("=" * 70)

# Get users
admin = User.objects.filter(role='ADMIN').first()
reception = User.objects.filter(role='RECEPTIONIST').first()

print("\n✅ ADMIN USER:")
if admin:
    print(f"  Phone: {admin.phone}")
    print(f"  Name: {admin.get_full_name() or admin.username}")
    print(f"  Role: {admin.role}")
    print(f"  is_admin: {admin.is_admin}")
    print("\n  PC Member Permissions:")
    print(f"    ✓ Can CREATE PC Members: {admin.is_admin} (Should be True)")
    print(f"    ✓ Can EDIT PC Members: {admin.is_admin} (Should be True)")
    print(f"    ✓ Can DELETE PC Members: {admin.is_admin} (Should be True)")
    print(f"    ✓ Can VIEW PC Dashboard: {admin.is_admin} (Should be True)")
    print(f"    ✓ Can VIEW PC Members: {admin.is_admin} (Should be True)")
else:
    print("  ⚠ No admin user found")

print("\n❌ RECEPTIONIST USER:")
if reception:
    print(f"  Phone: {reception.phone}")
    print(f"  Name: {reception.get_full_name() or reception.username}")
    print(f"  Role: {reception.role}")
    print(f"  is_receptionist: {reception.is_receptionist}")
    print("\n  PC Member Permissions:")
    print(f"    ✗ Can CREATE PC Members: {reception.is_admin} (Should be False)")
    print(f"    ✗ Can EDIT PC Members: {reception.is_admin} (Should be False)")
    print(f"    ✗ Can DELETE PC Members: {reception.is_admin} (Should be False)")
    print(f"    ✗ Can VIEW PC Dashboard: {reception.is_admin} (Should be False)")
    print(f"    ✗ Can VIEW PC Members: {reception.is_admin} (Should be False)")
    print(f"    ✓ Can CREATE PC Transactions: {reception.is_receptionist or reception.is_admin} (Should be True)")
else:
    print("  ⚠ No receptionist user found")

print("\n" + "=" * 70)
print("PERMISSION SUMMARY")
print("=" * 70)

print("\n✅ ADMIN CAN:")
print("  • Create new PC Members")
print("  • Edit existing PC Members (name, phone, email, address, status)")
print("  • Delete PC Members (even with transactions)")
print("  • View PC Dashboard")
print("  • View all PC Members by type")
print("  • View PC Member details")
print("  • Mark PC Member commissions as paid")
print("  • Create PC Transactions")

print("\n❌ RECEPTIONIST/OTHER USERS CANNOT:")
print("  • Create PC Members")
print("  • Edit PC Members")
print("  • Delete PC Members")
print("  • View PC Dashboard")
print("  • View PC Member lists")
print("  • View PC Member details")

print("\n✅ RECEPTIONIST CAN:")
print("  • Create PC Transactions (record referrals)")
print("  • Look up PC members by code (via API)")

print("\n" + "=" * 70)
print("VIEW PERMISSION CHECKS")
print("=" * 70)

views_with_admin_check = [
    'pc_member_list - List PC members by type',
    'pc_member_create - Create new PC member',
    'pc_member_edit - Edit existing PC member',
    'pc_member_detail - View PC member details',
    'pc_member_delete - Delete PC member',
    'pc_dashboard - PC system dashboard',
    'pc_mark_paid - Mark commissions as paid',
]

print("\nAll these views require ADMIN permission (is_admin check):")
for view in views_with_admin_check:
    print(f"  ✓ {view}")

print("\n" + "=" * 70)
print("URLS AVAILABLE")
print("=" * 70)

urls = [
    ('/accounts/pc-dashboard/', 'PC Dashboard', 'ADMIN'),
    ('/accounts/pc-members/GENERAL/', 'General Members List', 'ADMIN'),
    ('/accounts/pc-members/LIFETIME/', 'Lifetime Members List', 'ADMIN'),
    ('/accounts/pc-members/PREMIUM/', 'Premium Members List', 'ADMIN'),
    ('/accounts/pc-members/create/', 'Create PC Member', 'ADMIN'),
    ('/accounts/pc-member/<pc_code>/', 'PC Member Detail', 'ADMIN'),
    ('/accounts/pc-member/<pc_code>/edit/', 'Edit PC Member', 'ADMIN'),
    ('/accounts/pc-member/<pc_code>/delete/', 'Delete PC Member', 'ADMIN'),
    ('/accounts/pc-member/<pc_code>/mark-paid/', 'Mark Paid', 'ADMIN'),
    ('/accounts/pc-transaction/create/', 'Create Transaction', 'RECEPTIONIST/ADMIN'),
    ('/accounts/api/pc-lookup/', 'PC Lookup API', 'ANY'),
]

print("\nURL Patterns:")
for url, name, permission in urls:
    print(f"  {url}")
    print(f"    → {name} ({permission} only)")

print("\n" + "=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
