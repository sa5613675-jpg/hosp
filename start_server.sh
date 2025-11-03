#!/bin/bash
# Check and start server

cd /workspaces/hosp

echo "Checking server status..."

# Check if server is running
if pgrep -f "manage.py runserver" > /dev/null; then
    echo "✅ Server is already running"
    echo ""
    echo "Killing existing server..."
    pkill -f "manage.py runserver"
    sleep 2
fi

echo ""
echo "Starting Django server..."
echo "Server URL: http://localhost:8000"
echo "Admin Finance: http://localhost:8000/admin-finance/"
echo ""

python manage.py runserver 0.0.0.0:8000
