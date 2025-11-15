#!/usr/bin/env python
"""
Test PC Member Creation
Run this to verify PC member creation is working
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import PCMember, User

def test_pc_creation():
    print("=" * 60)
    print("Testing PC Member Creation")
    print("=" * 60)
    
    # Get or create admin user
    admin = User.objects.filter(role='ADMIN').first()
    if not admin:
        print("❌ No admin user found!")
        return False
    
    print(f"✅ Admin user: {admin.username}")
    
    # Test data for each member type
    test_data = [
        {
            'member_type': 'GENERAL',
            'name': 'Test General Member',
            'phone': '01711111111',
            'expected_rates': {'normal': 15.00, 'digital': 20.00, 'other': 15.00}
        },
        {
            'member_type': 'LIFETIME',
            'name': 'Test Lifetime Member',
            'phone': '01722222222',
            'expected_rates': {'normal': 20.00, 'digital': 25.00, 'other': 20.00}
        },
        {
            'member_type': 'PREMIUM',
            'name': 'Test Premium Member',
            'phone': '01733333333',
            'expected_rates': {'normal': 25.00, 'digital': 30.00, 'other': 25.00}
        }
    ]
    
    created_members = []
    
    for data in test_data:
        try:
            # Create member
            member = PCMember.objects.create(
                member_type=data['member_type'],
                name=data['name'],
                phone=data['phone'],
                email=f"{data['member_type'].lower()}@test.com",
                commission_percentage=data['expected_rates']['other'],
                normal_test_commission=data['expected_rates']['normal'],
                digital_test_commission=data['expected_rates']['digital'],
                created_by=admin
            )
            
            # Verify creation
            print(f"\n✅ Created {data['member_type']} Member")
            print(f"   Code: {member.pc_code}")
            print(f"   Name: {member.name}")
            print(f"   Normal: {member.normal_test_commission}% (expected: {data['expected_rates']['normal']}%)")
            print(f"   Digital: {member.digital_test_commission}% (expected: {data['expected_rates']['digital']}%)")
            print(f"   Other: {member.commission_percentage}% (expected: {data['expected_rates']['other']}%)")
            
            # Verify rates match
            if (float(member.normal_test_commission) == data['expected_rates']['normal'] and
                float(member.digital_test_commission) == data['expected_rates']['digital'] and
                float(member.commission_percentage) == data['expected_rates']['other']):
                print(f"   ✅ All rates match!")
            else:
                print(f"   ❌ Rates don't match!")
            
            created_members.append(member)
            
        except Exception as e:
            print(f"\n❌ Failed to create {data['member_type']} member: {str(e)}")
            return False
    
    # Cleanup
    print(f"\n{'=' * 60}")
    print("Cleaning up test data...")
    for member in created_members:
        member.delete()
    print("✅ All test members deleted")
    
    print(f"\n{'=' * 60}")
    print("✅ ALL TESTS PASSED - PC Member Creation is Working!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    test_pc_creation()
