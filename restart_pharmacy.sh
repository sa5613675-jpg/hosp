#!/bin/bash

echo "🛑 Stopping server..."
pkill -f "manage.py runserver"
sleep 2

echo "🚀 Starting server..."
cd /workspaces/hosp
/home/codespace/.python/current/bin/python manage.py runserver 0.0.0.0:8000
