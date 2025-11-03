#!/bin/bash
# Deploy doctor fee management feature

cd /workspaces/hosp

echo "=========================================="
echo "DEPLOYING DOCTOR FEE MANAGEMENT"
echo "=========================================="

# Test the feature
echo ""
echo "Step 1: Testing doctor fee management..."
python test_doctor_fee.py

if [ $? -ne 0 ]; then
    echo "❌ Test failed!"
    exit 1
fi

# Commit changes
echo ""
echo "Step 2: Committing changes..."
git add -A
git commit -m "Feature: Doctor fee management for admin

Changes:
- Added 'Consultation Fee' column to doctor management table
- Added inline edit button for each doctor's fee
- Created update_doctor_fee view to handle AJAX updates
- Added edit fee modal with validation
- Fee updates immediately without page reload
- Receptionist can use these fees during booking

Admin can now:
- View all doctors with their consultation fees
- Click edit button to update any doctor's fee
- Fee is saved and receptionist sees updated amount"

# Push to GitHub
echo ""
echo "Step 3: Pushing to GitHub..."
BRANCH=$(git branch --show-current)
git push origin $BRANCH || echo "⚠️ Push failed, continuing..."

# Start server
echo ""
echo "=========================================="
echo "Starting Django Server"
echo "=========================================="
echo ""
echo "Doctor Management: http://localhost:8000/accounts/doctor-management/"
echo ""

python manage.py runserver 0.0.0.0:8000
