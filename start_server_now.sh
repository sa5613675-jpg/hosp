#!/bin/bash

echo "========================================"
echo "STARTING DJANGO SERVER"
echo "========================================"

cd /workspaces/hosp

# Kill any existing server
echo "Stopping existing server..."
pkill -9 -f "manage.py runserver" 2>/dev/null
sleep 2

# Check for Django errors first
echo ""
echo "Checking Django configuration..."
/home/codespace/.python/current/bin/python manage.py check --deploy 2>&1 | head -20

echo ""
echo "Starting server on port 8000..."
echo ""

# Start server
/home/codespace/.python/current/bin/python manage.py runserver 0.0.0.0:8000
