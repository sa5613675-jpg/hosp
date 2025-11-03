#!/bin/bash
# Kill existing server and restart

cd /workspaces/hosp

echo "Stopping any running Django server..."
pkill -f "manage.py runserver"
sleep 2

echo ""
echo "Starting Django server..."
echo ""
echo "Access URLs:"
echo "- Admin Dashboard: http://localhost:8000/admin-dashboard/"
echo "- Pharmacy Management: http://localhost:8000/accounts/pharmacy-management/"
echo "- Finance Dashboard: http://localhost:8000/admin-finance/"
echo ""

python manage.py runserver 0.0.0.0:8000
