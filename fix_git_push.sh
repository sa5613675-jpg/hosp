#!/bin/bash
# Fix git push issues and push all changes

echo "==================================="
echo "FIX GIT PUSH & DEPLOY"
echo "==================================="

cd /workspaces/hosp

# Stage any unstaged changes
echo ""
echo "Step 1: Staging all changes..."
git add -A
echo "✅ All files staged"

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo ""
    echo "ℹ️  No changes to commit"
else
    echo ""
    echo "Step 2: Committing changes..."
    git commit -m "Fix: Expense save error and real-time profit display

Changes made:
- Fixed NoReverseMatch error in 6 finance templates
  * expense_form.html, expense_list.html
  * income_form.html, income_list.html  
  * invoice_form.html, invoice_list.html
- Added 'accounts:' namespace to admin_dashboard URLs
- Fixed profit variable in admin_finance.html template
- Admin can now save expenses successfully
- Real-time profit calculation displays correctly"
    
    echo "✅ Changes committed"
fi

# Get current branch
BRANCH=$(git branch --show-current)
echo ""
echo "Step 3: Current branch: $BRANCH"

# Try to push
echo ""
echo "Step 4: Pushing to GitHub..."
if git push origin $BRANCH; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo ""
    echo "⚠️  Standard push failed. Trying alternative methods..."
    
    # Try with --set-upstream
    echo ""
    echo "Trying: git push --set-upstream origin $BRANCH"
    if git push --set-upstream origin $BRANCH; then
        echo "✅ Successfully pushed with --set-upstream!"
    else
        echo ""
        echo "⚠️  Still having issues. Checking remote configuration..."
        git remote -v
        
        echo ""
        echo "Last resort: Trying force push (use with caution)..."
        echo "Command: git push --force origin $BRANCH"
        echo ""
        read -p "Do you want to force push? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push --force origin $BRANCH
            echo "✅ Force pushed!"
        else
            echo "❌ Push cancelled. Please check:"
            echo "   1. GitHub authentication (gh auth login)"
            echo "   2. Remote URL: git remote get-url origin"
            echo "   3. Branch permissions"
            exit 1
        fi
    fi
fi

echo ""
echo "==================================="
echo "✅ GIT PUSH COMPLETE!"
echo "==================================="
echo ""
echo "Repository: https://github.com/$GITHUB_USER/hosp"
echo "Branch: $BRANCH"
echo ""

# Ask to start server
echo "Do you want to start the Django server now?"
read -p "Start server? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting Django server on http://localhost:8000"
    echo ""
    python manage.py runserver 0.0.0.0:8000
fi
