#!/usr/bin/env python
"""Fix expense issues and test"""

import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp.settings')
django.setup()

from finance.models import Expense, ExpenseCategory, Department
from accounts.models import User
from django.utils import timezone

print("=" * 60)
print("FIXING EXPENSE ISSUES")
print("=" * 60)

# 1. Check if ExpenseCategory exists
print("\n1. Checking ExpenseCategory...")
category_count = ExpenseCategory.objects.count()
print(f"   Found {category_count} expense categories")

if category_count == 0:
    print("   Creating default categories...")
    categories = [
        {'name': 'Salary', 'description': 'Staff salaries and wages'},
        {'name': 'Utilities', 'description': 'Electricity, water, internet'},
        {'name': 'Equipment', 'description': 'Medical equipment and tools'},
        {'name': 'Supplies', 'description': 'Medical and office supplies'},
        {'name': 'Maintenance', 'description': 'Building and equipment maintenance'},
        {'name': 'Rent', 'description': 'Building rent'},
        {'name': 'Other', 'description': 'Miscellaneous expenses'},
    ]
    for cat_data in categories:
        ExpenseCategory.objects.create(**cat_data)
    print(f"   ✅ Created {len(categories)} default categories")
else:
    print("   ✅ Categories exist")

# 2. Check departments
print("\n2. Checking Departments...")
dept_count = Department.objects.count()
print(f"   Found {dept_count} departments")

if dept_count == 0:
    print("   Creating default department...")
    Department.objects.create(
        name='General',
        description='General Hospital Operations',
        is_active=True
    )
    print("   ✅ Created default department")

# 3. Get admin user
print("\n3. Finding admin user...")
admin = User.objects.filter(is_admin=True).first()
if not admin:
    print("   ❌ No admin user found!")
    exit(1)
print(f"   ✅ Admin: {admin.username}")

# 4. Test expense creation
print("\n4. Testing expense creation...")
try:
    test_expense = Expense.objects.create(
        expense_type='UTILITIES',
        amount=100.50,
        date=timezone.now().date(),
        description='Test expense - Electricity bill',
        recorded_by=admin,
        is_approved=True
    )
    print(f"   ✅ Created test expense: {test_expense.expense_number}")
    print(f"      Amount: ৳{test_expense.amount}")
    print(f"      Type: {test_expense.expense_type}")
    
    # Delete test expense
    test_expense.delete()
    print("   ✅ Test expense deleted")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 5. Count existing expenses
print("\n5. Checking existing expenses...")
total_expenses = Expense.objects.count()
print(f"   Total expenses in database: {total_expenses}")

if total_expenses > 0:
    print("\n   Recent expenses:")
    for exp in Expense.objects.all().order_by('-date')[:5]:
        print(f"   - {exp.expense_number}: ৳{exp.amount} ({exp.expense_type}) - {exp.date}")
else:
    print("   No expenses found yet")

# 6. Check URLs
print("\n6. Verifying URLs...")
try:
    from django.urls import reverse
    
    urls = [
        ('finance:expense_list', 'Expense List'),
        ('finance:expense_create', 'Create Expense'),
        ('accounts:quick_add_expense', 'Quick Add Expense'),
    ]
    
    for url_name, desc in urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {desc}: {url}")
        except Exception as e:
            print(f"   ❌ {desc}: {e}")
except Exception as e:
    print(f"   ❌ Error checking URLs: {e}")

print("\n" + "=" * 60)
print("✅ SETUP COMPLETE!")
print("=" * 60)
print("\nYou can now:")
print("1. Go to: http://localhost:8000/finance/expense/")
print("2. Click 'Add Expense' to create new expenses")
print("3. View all expenses in the list")
print("\nOr use the admin finance dashboard:")
print("4. Go to: http://localhost:8000/admin-finance/")
print("5. Click 'Add Expense' button in modal")
