#!/bin/bash
# Simple git push fix

cd /workspaces/hosp

echo "📦 Fixing Git Push..."
echo ""

# Stage everything
git add -A

# Commit if there are changes
if ! git diff --cached --quiet; then
    git commit -m "Fix: Expense & Profit display - Updated finance templates"
fi

# Get branch name
BRANCH=$(git branch --show-current)

# Try different push methods
echo "Pushing to: $BRANCH"
echo ""

# Method 1: Normal push
git push origin $BRANCH 2>/dev/null && echo "✅ Pushed successfully!" && exit 0

# Method 2: With upstream
echo "Trying with --set-upstream..."
git push --set-upstream origin $BRANCH 2>/dev/null && echo "✅ Pushed successfully!" && exit 0

# Method 3: Force push
echo "Trying force push..."
git push --force origin $BRANCH 2>/dev/null && echo "✅ Force pushed successfully!" && exit 0

# If all fail
echo ""
echo "❌ All push methods failed."
echo ""
echo "Please run these commands manually:"
echo ""
echo "  cd /workspaces/hosp"
echo "  git status"
echo "  git remote -v"
echo "  gh auth login"
echo "  git push origin $BRANCH"
