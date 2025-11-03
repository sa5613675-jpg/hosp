#!/bin/bash
# Start Hospital Management System on Port 8005

echo "═══════════════════════════════════════"
echo "  Starting Hospital System on Port 8005"
echo "═══════════════════════════════════════"

cd /var/www/hosp
source venv/bin/activate

# Kill any existing processes on port 8005
echo "→ Checking port 8005..."
if lsof -Pi :8005 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  Port 8005 is in use. Killing process..."
    sudo kill -9 $(lsof -t -i:8005) 2>/dev/null
    sleep 2
fi

# Kill any gunicorn processes for this app
if pgrep -f "gunicorn.*diagcenter" > /dev/null; then
    echo "→ Stopping existing gunicorn processes..."
    sudo pkill -f "gunicorn.*diagcenter"
    sleep 2
fi

# Start gunicorn on port 8005
echo "→ Starting Gunicorn on 0.0.0.0:8005..."
gunicorn diagcenter.wsgi:application \
    --bind 0.0.0.0:8005 \
    --workers 3 \
    --daemon \
    --access-logfile /var/log/hosp_access.log \
    --error-logfile /var/log/hosp_error.log \
    --pid /tmp/hosp_gunicorn.pid \
    --name hosp_diagcenter

if [ $? -eq 0 ]; then
    echo "✓ Gunicorn started successfully on port 8005"
    echo ""
    echo "Process ID saved to: /tmp/hosp_gunicorn.pid"
else
    echo "✗ Failed to start Gunicorn"
    exit 1
fi

# Wait a moment for startup
sleep 2

# Check if it's running
if curl -s http://localhost:8005 > /dev/null; then
    echo "✓ Hospital system is responding on port 8005"
else
    echo "⚠ Warning: Server started but not responding yet (may need a moment)"
fi

echo ""
echo "═══════════════════════════════════════"
echo "  ✓ Hospital System Running!"
echo "═══════════════════════════════════════"
echo ""
echo "Access at: http://your-ip:8005"
echo ""
echo "Commands:"
echo "  Check status:  ps aux | grep -i hosp"
echo "  View logs:     tail -f /var/log/hosp_error.log"
echo "  Stop server:   kill \$(cat /tmp/hosp_gunicorn.pid)"
echo "  Restart:       bash $0"
echo ""
echo "To configure Nginx proxy (optional):"
echo "  Add this to your nginx config:"
echo "  location /hospital {"
echo "      proxy_pass http://127.0.0.1:8005;"
echo "      proxy_set_header Host \$host;"
echo "  }"
echo ""
echo "═══════════════════════════════════════"
