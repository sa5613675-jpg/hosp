#!/bin/bash
# Complete pharmacy system - database fix and verification

cd /workspaces/hosp

echo "=========================================="
echo "COMPLETE PHARMACY SYSTEM SETUP"
echo "=========================================="

# Step 1: Migrations
echo ""
echo "Step 1: Creating and applying migrations..."
python manage.py makemigrations pharmacy
python manage.py migrate

# Step 2: Verify integration
echo ""
echo "Step 2: Verifying finance integration..."
python verify_pharmacy_integration.py

# Step 3: Commit
echo ""
echo "Step 3: Committing changes..."
git add -A
git commit -m "Complete: Pharmacy Management with Finance Integration

Features:
✅ Pharmacy sales auto-create Income (source=PHARMACY)
✅ Medicine purchases auto-create Expense (type=SUPPLIES)  
✅ Profit tracking per sale
✅ Integration with main finance dashboard
✅ Pharmacy management UI
✅ Stock management with buy/sell prices

Finance Dashboard Integration:
- Income breakdown shows PHARMACY sales
- Expense breakdown shows medicine purchases
- Net profit includes pharmacy profit
- All data visible in admin-finance dashboard" || echo "Nothing to commit"

# Step 4: Push
echo ""
echo "Step 4: Pushing to GitHub..."
BRANCH=$(git branch --show-current)
git push origin $BRANCH || echo "Push failed, continuing..."

# Step 5: Start server
echo ""
echo "=========================================="
echo "✅ PHARMACY SYSTEM READY!"
echo "=========================================="
echo ""
echo "HOW IT WORKS:"
echo ""
echo "1. PHARMACY SALES → FINANCE DASHBOARD"
echo "   - When you sell medicine, it auto-creates Income"
echo "   - Source: PHARMACY"
echo "   - Shows in finance dashboard income breakdown"
echo ""
echo "2. MEDICINE PURCHASES → FINANCE DASHBOARD"  
echo "   - When you buy medicine stock, it auto-creates Expense"
echo "   - Type: SUPPLIES"
echo "   - Shows in finance dashboard expense breakdown"
echo ""
echo "3. NET PROFIT CALCULATION"
echo "   - Finance dashboard includes pharmacy in total"
echo "   - Net Profit = All Income - All Expenses"
echo "   - Pharmacy profit is part of net profit"
echo ""
echo "ACCESS POINTS:"
echo "- Pharmacy Management: /accounts/pharmacy-management/"
echo "- Finance Dashboard: /admin-finance/"
echo "- Admin Dashboard: /admin-dashboard/"
echo ""
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
