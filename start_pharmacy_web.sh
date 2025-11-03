#!/bin/bash
cd /workspaces/hosp
pkill -9 -f "manage.py runserver" 2>/dev/null
sleep 2
/home/codespace/.python/current/bin/python manage.py runserver 0.0.0.0:8000 &
sleep 3
echo ""
echo "✅ Server Started!"
echo ""
echo "📍 Pharmacy Web Interface:"
echo "   • Dashboard:        http://localhost:8000/accounts/pharmacy-management/"
echo "   • Add Medicine:     http://localhost:8000/accounts/add-medicine/"
echo "   • View Medicines:   http://localhost:8000/accounts/view-medicines/"
echo "   • Add Stock:        http://localhost:8000/accounts/add-stock/"
echo ""
echo "✨ You can now add medicines from the website, not Django admin!"
