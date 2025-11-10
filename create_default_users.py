from django.contrib.auth import get_user_model
from accounts.models import PCMember
from decimal import Decimal

User = get_user_model()

# Create default users for different roles
default_users = [
    {
        'phone': '01332856002',
        'password': '123456',
        'name': 'Admin User',
        'is_active': True,
        'is_staff': True,
        'is_admin': True,
    },
    {
        'phone': '01712345678',
        'password': '123456',
        'name': 'Doctor One',
        'is_active': True,
        'is_doctor': True,
    },
    {
        'phone': '01812345678',
        'password': '123456',
        'name': 'Receptionist One',
        'is_active': True,
        'is_receptionist': True,
    },
    {
        'phone': '01912345678',
        'password': '123456',
        'name': 'Lab Staff One',
        'is_active': True,
        'is_lab_staff': True,
    },
    {
        'phone': '01612345678',
        'password': '123456',
        'name': 'Pharmacy Staff One',
        'is_active': True,
        'is_pharmacy_staff': True,
    }
]

# Create default PC Members
default_pc_members = [
    {
        'pc_code': '10001',
        'member_type': 'GENERAL',
        'name': 'Dr. Rahman',
        'phone': '01712345678',
        'commission_percentage': Decimal('20.00')
    },
    {
        'pc_code': '20001',
        'member_type': 'LIFETIME',
        'name': 'Dr. Fatima',
        'phone': '01812345678',
        'commission_percentage': Decimal('25.00')
    }
]

def create_default_users():
    for user_data in default_users:
        phone = user_data.pop('phone')
        password = user_data.pop('password')
        
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults=user_data
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"Created user with phone: {phone}")
        else:
            print(f"User with phone {phone} already exists")

def create_default_pc_members():
    for member_data in default_pc_members:
        pc_code = member_data['pc_code']
        member, created = PCMember.objects.get_or_create(
            pc_code=pc_code,
            defaults=member_data
        )
        if created:
            print(f"Created PC Member with code: {pc_code}")
        else:
            print(f"PC Member with code {pc_code} already exists")

if __name__ == '__main__':
    print("Creating default users...")
    create_default_users()
    print("\nCreating default PC Members...")
    create_default_pc_members()
    print("\nSetup complete!")
