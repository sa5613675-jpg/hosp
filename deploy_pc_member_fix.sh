#!/bin/bash

# Deploy PC Member CRUD Fixes to VPS
# Fixes: PC member create/edit/delete with proper admin permissions

echo "======================================================================"
echo "  PC MEMBER CRUD FIX DEPLOYMENT"
echo "======================================================================"
echo ""
echo "This script will:"
echo "  1. Pull latest code from GitHub"
echo "  2. Run database migrations (PCMember table)"
echo "  3. Collect static files"
echo "  4. Restart services"
echo ""
echo "Changes included:"
echo "  ✓ Fixed URL routing for PC member creation"
echo "  ✓ Added PC member edit functionality"
echo "  ✓ Admin-only permissions enforced"
echo "  ✓ Phone number uniqueness validation"
echo "  ✓ All CRUD operations working"
echo ""
read -p "Press ENTER to continue or CTRL+C to cancel..."

# Detect project directory
if [ -d "/root/hosp" ]; then
    PROJECT_DIR="/root/hosp"
elif [ -d "/var/www/hosp" ]; then
    PROJECT_DIR="/var/www/hosp"
else
    echo "Error: Could not find project directory!"
    echo "Trying current directory..."
    PROJECT_DIR=$(pwd)
fi

echo ""
echo "Using project directory: $PROJECT_DIR"

# Navigate to project
cd "$PROJECT_DIR" || exit 1

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found, using system Python"
fi

# Pull latest code
echo ""
echo "======================================================================"
echo "  Pulling latest code from GitHub..."
echo "======================================================================"
git fetch origin
git pull origin main

# Show what changed
echo ""
echo "Recent changes:"
git log --oneline -3

# Run migrations
echo ""
echo "======================================================================"
echo "  Running database migrations..."
echo "======================================================================"
python manage.py migrate accounts

# Collect static files
echo ""
echo "======================================================================"
echo "  Collecting static files..."
echo "======================================================================"
python manage.py collectstatic --noinput

# Restart services
echo ""
echo "======================================================================"
echo "  Restarting services..."
echo "======================================================================"

# Try different service names
if sudo systemctl is-active --quiet hosp; then
    echo "Restarting hosp service..."
    sudo systemctl restart hosp
elif sudo systemctl is-active --quiet gunicorn; then
    echo "Restarting gunicorn service..."
    sudo systemctl restart gunicorn
else
    echo "Warning: Could not find service to restart"
    echo "Please restart your Django service manually"
fi

# Restart nginx if available
if sudo systemctl is-active --quiet nginx; then
    echo "Restarting nginx..."
    sudo systemctl restart nginx
fi

# Check status
echo ""
echo "======================================================================"
echo "  Service Status:"
echo "======================================================================"
if sudo systemctl is-active --quiet hosp; then
    sudo systemctl status hosp --no-pager -l | head -15
elif sudo systemctl is-active --quiet gunicorn; then
    sudo systemctl status gunicorn --no-pager -l | head -15
fi

echo ""
echo "======================================================================"
echo "  ✅ DEPLOYMENT COMPLETE!"
echo "======================================================================"
echo ""
echo "PC Member System Changes:"
echo "  ✓ Create: /accounts/pc-members/create/"
echo "  ✓ List: /accounts/pc-members/GENERAL/ (or LIFETIME/PREMIUM)"
echo "  ✓ Edit: /accounts/pc-member/<code>/edit/"
echo "  ✓ Delete: /accounts/pc-member/<code>/delete/"
echo "  ✓ Detail: /accounts/pc-member/<code>/"
echo ""
echo "Member Types & Commission:"
echo "  • GENERAL (1xxxxx): Normal 15%, Digital 20%"
echo "  • LIFETIME (2xxxxx): Normal 20%, Digital 25%"
echo "  • PREMIUM (3xxxxx): Normal 25%, Digital 30%"
echo ""
echo "To test:"
echo "  1. Login as admin"
echo "  2. Go to PC Dashboard"
echo "  3. Click 'Add PC Member'"
echo "  4. Select member type and fill details"
echo "  5. Edit/Delete members from the list"
echo ""
echo "If you see any errors, check logs:"
echo "  sudo journalctl -u hosp -n 50"
echo "  or"
echo "  sudo journalctl -u gunicorn -n 50"
echo ""
echo "======================================================================"
