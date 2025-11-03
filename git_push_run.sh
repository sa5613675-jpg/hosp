#!/bin/bash
# Commit and push changes, then start server

cd /workspaces/hosp

# Stage all
git add -A

# Commit
git commit -m "Fix: Expense save error and real-time profit display - All finance templates updated with correct URL namespaces"

# Push
git push origin $(git branch --show-current)

# Start server
echo ""
echo "✅ Changes pushed! Starting server..."
echo ""
python manage.py runserver 0.0.0.0:8000
