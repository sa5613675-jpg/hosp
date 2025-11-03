#!/bin/bash
# Fix expense and start server

cd /workspaces/hosp

echo "=========================================="
echo "FIXING EXPENSE SYSTEM"
echo "=========================================="

# Run fix
python fix_expense_system.py

# Commit
git add -A
git commit -m "Fix: Expense creation and listing" || true

# Push
git push origin $(git branch --show-current) || true

echo ""
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
