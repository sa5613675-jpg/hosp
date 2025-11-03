#!/bin/bash
# Diagnose and fix git push issues

echo "==================================="
echo "GIT PUSH DIAGNOSTICS"
echo "==================================="
echo ""

# Check current branch
echo "1. Current branch:"
git branch --show-current
echo ""

# Check git status
echo "2. Git status:"
git status
echo ""

# Check remote
echo "3. Remote configuration:"
git remote -v
echo ""

# Check unpushed commits
echo "4. Unpushed commits:"
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || echo "   No unpushed commits or remote branch doesn't exist"
echo ""

# Try to push
echo "5. Attempting to push..."
git push origin $(git branch --show-current) 2>&1

EXIT_CODE=$?
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Push failed with exit code: $EXIT_CODE"
    echo ""
    echo "Possible solutions:"
    echo "1. Check your GitHub authentication"
    echo "2. Verify remote URL is correct"
    echo "3. Try: git push -u origin $(git branch --show-current)"
    echo "4. Try: git push --force origin $(git branch --show-current)"
fi
