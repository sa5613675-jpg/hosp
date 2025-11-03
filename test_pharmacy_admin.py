#!/usr/bin/env python
"""Test pharmacy admin registration and database schema"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp.settings')
sys.path.insert(0, '/workspaces/hosp')
django.setup()

from django.contrib import admin
from pharmacy.models import Drug, PharmacySale, SaleItem, StockAdjustment, DrugCategory

def test_admin_registration():
    """Check if pharmacy models are registered in admin"""
    print("=" * 60)
    print("TESTING PHARMACY ADMIN REGISTRATION")
    print("=" * 60)
    
    registered_models = admin.site._registry
    
    models_to_check = [
        (DrugCategory, 'DrugCategory'),
        (Drug, 'Drug'),
        (PharmacySale, 'PharmacySale'),
        (SaleItem, 'SaleItem'),
        (StockAdjustment, 'StockAdjustment'),
    ]
    
    all_registered = True
    for model, name in models_to_check:
        if model in registered_models:
            print(f"✅ {name} is registered in admin")
        else:
            print(f"❌ {name} is NOT registered in admin")
            all_registered = False
    
    return all_registered

def test_database_schema():
    """Check if all required fields exist in database"""
    print("\n" + "=" * 60)
    print("TESTING DATABASE SCHEMA")
    print("=" * 60)
    
    from django.db import connection
    
    tables_to_check = {
        'pharmacy_drug': ['buy_price'],
        'pharmacy_pharmacysale': ['total_profit', 'income_created'],
        'pharmacy_saleitem': ['buy_price', 'profit'],
        'pharmacy_stockadjustment': ['expense_created'],
    }
    
    all_columns_exist = True
    
    with connection.cursor() as cursor:
        for table, required_columns in tables_to_check.items():
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            
            print(f"\n📋 Table: {table}")
            for col in required_columns:
                if col in columns:
                    print(f"  ✅ Column '{col}' exists")
                else:
                    print(f"  ❌ Column '{col}' MISSING")
                    all_columns_exist = False
    
    return all_columns_exist

def test_model_functionality():
    """Test if models can be queried"""
    print("\n" + "=" * 60)
    print("TESTING MODEL FUNCTIONALITY")
    print("=" * 60)
    
    try:
        # Test Drug model
        drug_count = Drug.objects.count()
        print(f"✅ Drug model works - {drug_count} records")
        
        # Test PharmacySale model with new fields
        from django.db.models import Sum
        sales = PharmacySale.objects.all()
        total_profit = sales.aggregate(Sum('total_profit'))['total_profit__sum'] or 0
        print(f"✅ PharmacySale model works - {sales.count()} sales, ৳{total_profit} total profit")
        
        # Test SaleItem model
        items = SaleItem.objects.count()
        print(f"✅ SaleItem model works - {items} items sold")
        
        # Test StockAdjustment model
        adjustments = StockAdjustment.objects.count()
        print(f"✅ StockAdjustment model works - {adjustments} adjustments")
        
        return True
    except Exception as e:
        print(f"❌ Model query failed: {e}")
        return False

def main():
    print("\n🔍 PHARMACY SYSTEM DIAGNOSTIC TEST\n")
    
    admin_ok = test_admin_registration()
    schema_ok = test_database_schema()
    models_ok = test_model_functionality()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Admin Registration: {'✅ PASS' if admin_ok else '❌ FAIL'}")
    print(f"Database Schema:    {'✅ PASS' if schema_ok else '❌ FAIL'}")
    print(f"Model Functionality: {'✅ PASS' if models_ok else '❌ FAIL'}")
    
    if admin_ok and schema_ok and models_ok:
        print("\n🎉 ALL TESTS PASSED! Pharmacy system is ready.")
        print("\n📝 Next steps:")
        print("   1. Access admin at: http://localhost:8000/admin/pharmacy/drug/")
        print("   2. Add medicines from the admin panel")
        print("   3. View dashboard at: http://localhost:8000/accounts/pharmacy-management/")
    else:
        print("\n⚠️  SOME TESTS FAILED! Please run:")
        print("   chmod +x fix_pharmacy_complete.sh && ./fix_pharmacy_complete.sh")
    
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
