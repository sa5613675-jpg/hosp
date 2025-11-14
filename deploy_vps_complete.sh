#!/bin/bash

# Complete VPS Update Script
# Fixes all errors: test_type column, queue_display template, patient_delete, PC codes

echo "======================================================================"
echo "  HOSPITAL MANAGEMENT SYSTEM - VPS UPDATE"
echo "======================================================================"
echo ""
echo "This script will:"
echo "  1. Pull latest code from GitHub"
echo "  2. Fix lab_labtest.test_type column error"
echo "  3. Fix PC member codes (5-digit to 6-digit)"
echo "  4. Run all migrations"
echo "  5. Collect static files"
echo "  6. Restart services"
echo ""
read -p "Press ENTER to continue or CTRL+C to cancel..."

# Navigate to project
cd /root/hosp || exit 1

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Pull latest code
echo ""
echo "Pulling latest code from GitHub..."
git pull origin main

# Fix test_type column
echo ""
echo "======================================================================"
echo "  FIX 1: Adding missing lab_labtest.test_type column"
echo "======================================================================"
bash fix_vps_labtest.sh

# Fix PC codes
echo ""
echo "======================================================================"
echo "  FIX 2: Updating PC codes to 6-digit format"
echo "======================================================================"
python fix_pc_codes.py

# Run migrations
echo ""
echo "======================================================================"
echo "  Running database migrations..."
echo "======================================================================"
python manage.py migrate

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
sudo systemctl restart hosp
sudo systemctl restart nginx

# Check status
echo ""
echo "======================================================================"
echo "  Service Status:"
echo "======================================================================"
sudo systemctl status hosp --no-pager -l | head -20

echo ""
echo "======================================================================"
echo "  ✅ UPDATE COMPLETE!"
echo "======================================================================"
echo ""
echo "Changes applied:"
echo "  ✓ Lab test_type column added"
echo "  ✓ PC codes updated to 6-digit format"
echo "  ✓ Queue display template added"
echo "  ✓ Patient delete functionality added"
echo "  ✓ All migrations applied"
echo "  ✓ Static files collected"
echo "  ✓ Services restarted"
echo ""
echo "Please verify:"
echo "  - Homepage: http://your-server-ip/"
echo "  - PC Dashboard: http://your-server-ip/accounts/pc-members/GENERAL/"
echo "  - Lab Registration: http://your-server-ip/lab/quick-registration/"
echo "  - Patient Queue: http://your-server-ip/appointments/queue/"
echo ""
echo "If you see any errors, check logs:"
echo "  sudo journalctl -u hosp -n 50"
echo ""
echo "======================================================================"
