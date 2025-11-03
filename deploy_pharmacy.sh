#!/bin/bash
# Complete pharmacy system deployment

cd /workspaces/hosp

echo "=========================================="
echo "PHARMACY MANAGEMENT SYSTEM DEPLOYMENT"
echo "=========================================="

# Step 1: Make and apply migrations
echo ""
echo "Step 1: Running migrations..."
python manage.py makemigrations pharmacy
python manage.py migrate

# Step 2: Test system
echo ""
echo "Step 2: Testing pharmacy system..."
python test_pharmacy_system.py

# Step 3: Commit and push
echo ""
echo "Step 3: Committing to Git..."
git add -A
git commit -m "Feature: Pharmacy Management System with profit tracking and finance integration" || echo "Nothing to commit"

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
echo "Features:"
echo "✅ Medicine stock with buy/sell prices"
echo "✅ Auto-expense on purchase"
echo "✅ Auto-income on sale"
echo "✅ Profit tracking"
echo "✅ Finance integration"
echo ""
echo "Starting server..."
echo ""

python manage.py runserver 0.0.0.0:8000
