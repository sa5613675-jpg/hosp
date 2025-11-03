#!/bin/bash
# Fix pharmacy database and start server

cd /workspaces/hosp

echo "=========================================="
echo "FIXING PHARMACY DATABASE"
echo "=========================================="

# Step 1: Create migrations
echo ""
echo "Step 1: Creating migrations..."
python manage.py makemigrations pharmacy

# Step 2: Apply migrations
echo ""
echo "Step 2: Applying migrations..."
python manage.py migrate

echo ""
echo "✅ Database updated!"
echo ""
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
