from django.contrib.auth import get_user_model
from accounts.models import PCMember
from decimal import Decimal

User = get_user_model()

# Create initial admin user
admin_user = {
    'phone': '01332856002',
    'password': 'admin123',
    'name': 'Super Admin',
    'is_active': True,
    'is_staff': True,
    'is_admin': True,
}

# Create the admin user
def create_admin():
    user, created = User.objects.get_or_create(
        phone=admin_user['phone'],
        defaults={
            'name': admin_user['name'],
            'is_active': admin_user['is_active'],
            'is_staff': admin_user['is_staff'],
            'is_admin': admin_user['is_admin']
        }
    )
    if created:
        user.set_password(admin_user['password'])
        user.save()
        print(f"Created admin user with phone: {admin_user['phone']}")
    else:
        print(f"Admin user already exists")

if __name__ == '__main__':
    print("Creating admin user...")
    create_admin()
    print("\nSetup complete!")
    print("\nYou can login with:")
    print(f"Phone: {admin_user['phone']}")
    print(f"Password: {admin_user['password']}")