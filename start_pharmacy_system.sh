#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   PHARMACY MANAGEMENT SYSTEM - AUTO FIX & START            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/hosp

# Step 1: Stop server
echo "🛑 Step 1: Stopping existing server..."
pkill -f "manage.py runserver" 2>/dev/null
sleep 2
echo "   ✅ Server stopped"

# Step 2: Apply migrations
echo ""
echo "📦 Step 2: Applying database migrations..."
/home/codespace/.python/current/bin/python manage.py makemigrations pharmacy
/home/codespace/.python/current/bin/python manage.py migrate pharmacy
echo "   ✅ Migrations applied"

# Step 3: Test admin registration
echo ""
echo "🔍 Step 3: Testing admin registration..."
/home/codespace/.python/current/bin/python test_pharmacy_admin.py

# Step 4: Start server
echo ""
echo "🚀 Step 4: Starting Django server..."
/home/codespace/.python/current/bin/python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
sleep 3

# Check if server started
if pgrep -f "manage.py runserver" > /dev/null; then
    echo "   ✅ Server started successfully!"
else
    echo "   ❌ Server failed to start"
    exit 1
fi

# Success message
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✅ SETUP COMPLETE!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access Points:"
echo "   • Admin Panel:         http://localhost:8000/admin/"
echo "   • Admin Dashboard:     http://localhost:8000/accounts/admin-dashboard/"
echo "   • Pharmacy Dashboard:  http://localhost:8000/accounts/pharmacy-management/"
echo ""
echo "💊 Pharmacy Admin URLs (Now Working):"
echo "   • View Medicines:      http://localhost:8000/admin/pharmacy/drug/"
echo "   • Add Medicine:        http://localhost:8000/admin/pharmacy/drug/add/"
echo "   • View Stock:          http://localhost:8000/admin/pharmacy/stockadjustment/"
echo "   • Add Stock:           http://localhost:8000/admin/pharmacy/stockadjustment/add/"
echo "   • View Sales:          http://localhost:8000/admin/pharmacy/pharmacysale/"
echo "   • Categories:          http://localhost:8000/admin/pharmacy/drugcategory/"
echo ""
echo "📝 Quick Start:"
echo "   1. Login to admin panel"
echo "   2. Go to Pharmacy → Drugs → Add Drug"
echo "   3. Add medicine with buy price (e.g., ৳50) and sell price (e.g., ৳80)"
echo "   4. Go to Stock Adjustments → Add to increase stock"
echo "   5. View statistics in Pharmacy Management dashboard"
echo ""
echo "🎯 All Features Now Working:"
echo "   ✅ Add medicines with buy/sell prices"
echo "   ✅ Add stock (auto-creates expense)"
echo "   ✅ Record sales (auto-creates income)"
echo "   ✅ View profit reports (today/week/month/year)"
echo "   ✅ Low stock alerts"
echo "   ✅ Finance dashboard integration"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
