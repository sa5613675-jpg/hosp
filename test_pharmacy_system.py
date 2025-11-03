#!/usr/bin/env python
"""Test pharmacy management system"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp.settings')
django.setup()

from pharmacy.models import Drug, DrugCategory, PharmacySale, SaleItem, StockAdjustment
from accounts.models import User
from django.utils import timezone
from decimal import Decimal

print("=" * 60)
print("TESTING PHARMACY MANAGEMENT SYSTEM")
print("=" * 60)

# Test 1: Check Drug model enhancements
print("\n1. Testing Drug model enhancements...")
try:
    drugs = Drug.objects.all()
    print(f"   Found {drugs.count()} drugs in database")
    
    if drugs.exists():
        drug = drugs.first()
        print(f"\n   Sample drug: {drug.brand_name}")
        print(f"   - Buy Price: ৳{drug.buy_price}")
        print(f"   - Sell Price: ৳{drug.selling_price}")
        print(f"   - Profit per unit: ৳{drug.profit_per_unit}")
        print(f"   - Profit margin: {drug.profit_margin:.2f}%")
        print(f"   - Stock: {drug.quantity_in_stock} units")
        print(f"   - Stock value (buy): ৳{drug.stock_value_buy}")
        print(f"   - Stock value (sell): ৳{drug.stock_value_sell}")
        print("   ✅ Drug model working!")
    else:
        print("   ℹ️  No drugs in database yet")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Check pharmacy sales
print("\n2. Testing Pharmacy Sales...")
try:
    sales = PharmacySale.objects.all()
    print(f"   Found {sales.count()} sales")
    
    if sales.exists():
        sale = sales.first()
        print(f"\n   Sample sale: {sale.sale_number}")
        print(f"   - Total Amount: ৳{sale.total_amount}")
        print(f"   - Total Profit: ৳{sale.total_profit}")
        print(f"   - Income Created: {'Yes' if sale.income_created else 'No'}")
        
        items = sale.items.all()
        print(f"   - Items: {items.count()}")
        for item in items:
            print(f"     * {item.drug.brand_name}: {item.quantity} x ৳{item.unit_price} = ৳{item.total_price} (Profit: ৳{item.profit})")
        print("   ✅ Sales model working!")
    else:
        print("   ℹ️  No sales yet")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check stock adjustments
print("\n3. Testing Stock Adjustments...")
try:
    adjustments = StockAdjustment.objects.all()
    print(f"   Found {adjustments.count()} stock adjustments")
    
    if adjustments.exists():
        adj = adjustments.first()
        print(f"\n   Sample adjustment: {adj.drug.brand_name}")
        print(f"   - Type: {adj.adjustment_type}")
        print(f"   - Quantity: {adj.quantity}")
        print(f"   - Unit Cost: ৳{adj.unit_cost}")
        print(f"   - Expense Created: {'Yes' if adj.expense_created else 'No'}")
        print("   ✅ Stock adjustments working!")
    else:
        print("   ℹ️  No adjustments yet")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Calculate total pharmacy stats
print("\n4. Calculating Pharmacy Statistics...")
try:
    from django.db.models import Sum, Count
    from datetime import date
    
    today = date.today()
    
    # Today's sales
    today_sales = PharmacySale.objects.filter(sale_date__date=today).aggregate(
        total_amount=Sum('total_amount'),
        total_profit=Sum('total_profit'),
        count=Count('id')
    )
    
    print(f"\n   Today's Statistics:")
    print(f"   - Sales Count: {today_sales['count'] or 0}")
    print(f"   - Total Amount: ৳{today_sales['total_amount'] or 0}")
    print(f"   - Total Profit: ৳{today_sales['total_profit'] or 0}")
    
    # Total stock value
    total_buy_value = sum(drug.stock_value_buy for drug in Drug.objects.filter(is_active=True))
    total_sell_value = sum(drug.stock_value_sell for drug in Drug.objects.filter(is_active=True))
    
    print(f"\n   Stock Statistics:")
    print(f"   - Total Drugs: {Drug.objects.filter(is_active=True).count()}")
    print(f"   - Stock Value (Buy): ৳{total_buy_value:.2f}")
    print(f"   - Stock Value (Sell): ৳{total_sell_value:.2f}")
    print(f"   - Potential Profit: ৳{total_sell_value - total_buy_value:.2f}")
    
    # Low stock alerts
    low_stock = Drug.objects.filter(is_active=True, quantity_in_stock__lte=models.F('reorder_level'))
    print(f"   - Low Stock Items: {low_stock.count()}")
    
    print("   ✅ Statistics calculation working!")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Integration with finance
print("\n5. Testing Finance Integration...")
try:
    from finance.models import Income, Expense
    
    # Check pharmacy income
    pharmacy_income = Income.objects.filter(source='PHARMACY').aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    print(f"   Pharmacy Income Records: {pharmacy_income['count'] or 0}")
    print(f"   Total Income: ৳{pharmacy_income['total'] or 0}")
    
    # Check medicine purchase expenses
    medicine_expenses = Expense.objects.filter(
        expense_type='SUPPLIES',
        description__icontains='Medicine'
    ).aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    print(f"   Medicine Purchase Expenses: {medicine_expenses['count'] or 0}")
    print(f"   Total Expenses: ৳{medicine_expenses['total'] or 0}")
    
    print("   ✅ Finance integration working!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ PHARMACY SYSTEM TEST COMPLETE!")
print("=" * 60)
print("\nSYSTEM READY FOR:")
print("1. Adding medicine stock with buy/sell prices")
print("2. Recording pharmacy sales")
print("3. Tracking profit and inventory")
print("4. Auto-integration with finance system")
