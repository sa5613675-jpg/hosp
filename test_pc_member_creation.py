#!/usr/bin/env python
"""
Test PC Member Creation
Tests the complete flow of creating PC members through the view
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.messages import get_messages
from accounts.models import PCMember, User
from accounts.pc_views import pc_member_create

def test_pc_member_creation():
    print("=" * 60)
    print("PC MEMBER CREATION TEST")
    print("=" * 60)
    
    # Get or create admin user
    admin = User.objects.filter(role='ADMIN').first()
    if not admin:
        admin = User.objects.create_user(
            username='testadmin',
            password='admin123',
            role='ADMIN',
            first_name='Test',
            last_name='Admin'
        )
        print(f"✓ Created admin user: {admin}")
    else:
        print(f"✓ Using admin user: {admin}")
    
    # Initialize client
    client = Client()
    client.force_login(admin)
    
    print("\n" + "=" * 60)
    print("TEST 1: Create GENERAL member")
    print("=" * 60)
    
    response = client.post('/accounts/pc-members/create/', {
        'member_type': 'GENERAL',
        'name': 'Web Test General',
        'phone': '01711111111',
        'email': 'webtest1@example.com',
        'address': 'Test Address 1',
        'notes': 'Created via web test',
        'is_active': 'on'
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Redirect URL: {response.url if response.status_code == 302 else 'N/A'}")
    
    # Check messages
    messages = list(get_messages(response.wsgi_request))
    for msg in messages:
        print(f"Message ({msg.level_tag}): {msg}")
    
    # Check if member was created
    member = PCMember.objects.filter(phone='01711111111').first()
    if member:
        print(f"✓ Member created: {member.pc_code} - {member.name}")
        print(f"  Type: {member.get_member_type_display()}")
        print(f"  Commission: Normal {member.normal_test_commission}%, Digital {member.digital_test_commission}%")
    else:
        print("✗ Member NOT created")
    
    print("\n" + "=" * 60)
    print("TEST 2: Create LIFETIME member")
    print("=" * 60)
    
    response = client.post('/accounts/pc-members/create/', {
        'member_type': 'LIFETIME',
        'name': 'Web Test Lifetime',
        'phone': '01722222222',
        'email': 'webtest2@example.com',
        'is_active': 'on'
    })
    
    print(f"Response status: {response.status_code}")
    messages = list(get_messages(response.wsgi_request))
    for msg in messages:
        print(f"Message ({msg.level_tag}): {msg}")
    
    member = PCMember.objects.filter(phone='01722222222').first()
    if member:
        print(f"✓ Member created: {member.pc_code} - {member.name}")
    else:
        print("✗ Member NOT created")
    
    print("\n" + "=" * 60)
    print("TEST 3: Create PREMIUM member")
    print("=" * 60)
    
    response = client.post('/accounts/pc-members/create/', {
        'member_type': 'PREMIUM',
        'name': 'Web Test Premium',
        'phone': '01733333333',
        'is_active': 'on'
    })
    
    print(f"Response status: {response.status_code}")
    messages = list(get_messages(response.wsgi_request))
    for msg in messages:
        print(f"Message ({msg.level_tag}): {msg}")
    
    member = PCMember.objects.filter(phone='01733333333').first()
    if member:
        print(f"✓ Member created: {member.pc_code} - {member.name}")
    else:
        print("✗ Member NOT created")
    
    print("\n" + "=" * 60)
    print("TEST 4: Duplicate phone number")
    print("=" * 60)
    
    response = client.post('/accounts/pc-members/create/', {
        'member_type': 'GENERAL',
        'name': 'Duplicate Test',
        'phone': '01711111111',  # Same as first test
        'is_active': 'on'
    })
    
    print(f"Response status: {response.status_code}")
    messages = list(get_messages(response.wsgi_request))
    for msg in messages:
        print(f"Message ({msg.level_tag}): {msg}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total PC Members: {PCMember.objects.count()}")
    for m in PCMember.objects.all().order_by('pc_code'):
        print(f"  {m.pc_code}: {m.name} ({m.get_member_type_display()}) - {m.phone}")

if __name__ == '__main__':
    test_pc_member_creation()
