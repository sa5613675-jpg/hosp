#!/bin/bash
# Quick service restart script for VPS

echo "Checking running services..."

# Check what's running
if pgrep -f "gunicorn" > /dev/null; then
    echo "✓ Gunicorn is running"
    echo "→ Killing gunicorn processes..."
    sudo pkill -f gunicorn
    sleep 2
fi

if pgrep -f "python manage.py runserver" > /dev/null; then
    echo "✓ Django runserver is running"
    echo "→ Killing runserver processes..."
    sudo pkill -f "python manage.py runserver"
    sleep 2
fi

# Start gunicorn
echo "→ Starting Gunicorn..."
cd /var/www/hosp
source venv/bin/activate

# Start gunicorn in background
gunicorn diagcenter.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon \
    --access-logfile /var/log/hosp_access.log \
    --error-logfile /var/log/hosp_error.log \
    --pid /tmp/gunicorn.pid

if [ $? -eq 0 ]; then
    echo "✓ Gunicorn started successfully"
else
    echo "✗ Failed to start Gunicorn"
    exit 1
fi

# Reload nginx
if systemctl is-active --quiet nginx; then
    echo "→ Reloading Nginx..."
    sudo systemctl reload nginx
    echo "✓ Nginx reloaded"
else
    echo "⚠ Nginx is not running. Starting it..."
    sudo systemctl start nginx
fi

echo ""
echo "═══════════════════════════════════════"
echo "  ✓ Services restarted!"
echo "═══════════════════════════════════════"
echo ""
echo "Check status:"
echo "  ps aux | grep gunicorn"
echo "  sudo systemctl status nginx"
echo ""
echo "View logs:"
echo "  tail -f /var/log/hosp_error.log"
echo "  tail -f /var/log/nginx/error.log"
echo ""
