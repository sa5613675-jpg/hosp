#!/bin/bash

echo "=========================================="
echo "Pharmacy System Complete Fix"
echo "=========================================="

cd /workspaces/hosp

# Kill any running server
echo "Stopping existing server..."
pkill -f "manage.py runserver" 2>/dev/null
sleep 2

# Check migrations status
echo ""
echo "Checking migrations..."
/home/codespace/.python/current/bin/python manage.py showmigrations pharmacy

# Apply migrations
echo ""
echo "Applying migrations..."
/home/codespace/.python/current/bin/python manage.py makemigrations pharmacy
/home/codespace/.python/current/bin/python manage.py migrate pharmacy

# Verify database columns
echo ""
echo "Verifying database schema..."
/home/codespace/.python/current/bin/python manage.py dbshell <<EOF
.schema pharmacy_drug
.schema pharmacy_pharmacysale
.schema pharmacy_saleitem
.schema pharmacy_stockadjustment
.quit
EOF

# Start server
echo ""
echo "Starting Django server..."
/home/codespace/.python/current/bin/python manage.py runserver 0.0.0.0:8000 &

sleep 3

echo ""
echo "=========================================="
echo "✅ Server started successfully!"
echo "=========================================="
echo "Access at: http://localhost:8000"
echo ""
echo "Pharmacy Admin URLs should now work:"
echo "- View Medicines: http://localhost:8000/admin/pharmacy/drug/"
echo "- Add Medicine: http://localhost:8000/admin/pharmacy/drug/add/"
echo "- Stock Adjustments: http://localhost:8000/admin/pharmacy/stockadjustment/"
echo "- Add Stock: http://localhost:8000/admin/pharmacy/stockadjustment/add/"
echo "- Pharmacy Sales: http://localhost:8000/admin/pharmacy/pharmacysale/"
echo ""
echo "Pharmacy Management Dashboard:"
echo "- http://localhost:8000/accounts/pharmacy-management/"
echo ""
