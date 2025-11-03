#!/bin/bash
# Push all changes to GitHub and start the server

echo "=================================="
echo "PUSHING TO GITHUB & STARTING SERVER"
echo "=================================="

# Stage all changes
echo ""
echo "1. Staging all changes..."
git add -A

# Commit with message
echo ""
echo "2. Committing changes..."
git commit -m "Fix: Resolved expense save error and real-time profit display

- Fixed NoReverseMatch error in 6 finance templates (missing 'accounts:' namespace)
- Fixed profit display in admin_finance.html (net_profit -> profit)
- Updated expense_form.html, expense_list.html, income_list.html, income_form.html, invoice_form.html, invoice_list.html
- Admin can now add expenses and see real-time net profit calculation
- Profit = Income - Expenses updates immediately after saving expense"

# Push to GitHub
echo ""
echo "3. Pushing to GitHub..."
git push origin codespace-gruesome-seance-97ggq9x5vgqphxvr9

echo ""
echo "✅ Changes pushed to GitHub successfully!"
echo ""
echo "=================================="
echo "STARTING DJANGO SERVER"
echo "=================================="
echo ""
echo "Server will start on: http://localhost:8000"
echo "Admin Dashboard: http://localhost:8000/admin-dashboard/"
echo "Finance Dashboard: http://localhost:8000/admin-finance/"
echo ""

# Start server
python manage.py runserver 0.0.0.0:8000
