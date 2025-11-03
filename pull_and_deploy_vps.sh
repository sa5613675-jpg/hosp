#!/bin/bash
# Pull and Deploy on VPS
# Run this on your Ubuntu VPS

echo "════════════════════════════════════════════════════════════"
echo "  Pulling Latest Production Code from GitHub"
echo "════════════════════════════════════════════════════════════"

# Navigate to your app directory (adjust if different)
cd /var/www/diagcenter || cd /home/ubuntu/hosp || cd ~/hosp || exit 1

echo "✓ In directory: $(pwd)"
echo ""

# Pull latest code from main branch
echo "→ Pulling from GitHub (main branch)..."
git fetch origin main
git reset --hard origin/main

echo "✓ Code updated"
echo ""

# Clean Python cache
echo "→ Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
echo "✓ Cache cleaned"
echo ""

# Activate virtual environment (adjust path if different)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ No virtual environment found. Using system Python."
fi
echo ""

# Install/update dependencies
echo "→ Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies updated"
echo ""

# Run migrations
echo "→ Running database migrations..."
python manage.py migrate
echo "✓ Migrations complete"
echo ""

# Collect static files
echo "→ Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Restart services
echo "→ Restarting services..."

if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart diagcenter
    echo "✓ Supervisor restarted"
fi

if systemctl is-active --quiet gunicorn; then
    sudo systemctl restart gunicorn
    echo "✓ Gunicorn restarted"
fi

if systemctl is-active --quiet nginx; then
    sudo systemctl reload nginx
    echo "✓ Nginx reloaded"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✓ DEPLOYMENT COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Your application is now running with the latest code."
echo ""
echo "Check status:"
echo "  sudo supervisorctl status diagcenter"
echo "  sudo systemctl status nginx"
echo ""
echo "View logs:"
echo "  tail -f /var/log/diagcenter/gunicorn_error.log"
echo ""
echo "════════════════════════════════════════════════════════════"
