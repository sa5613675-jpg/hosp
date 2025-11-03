#!/bin/bash
# Complete deployment: Push to GitHub and start server

echo "=========================================="
echo "DEPLOYMENT: Push to GitHub & Start Server"
echo "=========================================="

cd /workspaces/hosp

# Stage all changes
echo ""
echo "Step 1: Staging changes..."
git add -A
echo "✅ Files staged"

# Commit
echo ""
echo "Step 2: Committing..."
git commit -m "Fix: Expense modal save functionality

Changes:
- Created quick_add_expense view in accounts/views.py
- Added URL route: accounts:quick_add_expense
- Updated admin_finance.html modal to use new endpoint
- Fixed expense creation from finance dashboard modal
- Expenses now save correctly and auto-approve
- Real-time profit updates after expense save

Bug fixed: Modal form was posting to wrong endpoint with mismatched fields
Solution: Created dedicated quick-add endpoint that handles modal form data"

# Push
echo ""
echo "Step 3: Pushing to GitHub..."
BRANCH=$(git branch --show-current)
git push origin $BRANCH

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "⚠️ Push may have failed, but continuing..."
fi

# Start server
echo ""
echo "=========================================="
echo "Starting Django Development Server"
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  http://localhost:8000"
echo ""
echo "Admin Finance Dashboard:"
echo "  http://localhost:8000/admin-finance/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 0.0.0.0:8000
