#!/bin/bash
# Stop Hospital Management System

echo "Stopping Hospital System..."

# Kill process by PID file
if [ -f /tmp/hosp_gunicorn.pid ]; then
    PID=$(cat /tmp/hosp_gunicorn.pid)
    if ps -p $PID > /dev/null; then
        echo "→ Killing process $PID..."
        kill $PID
        sleep 2
        # Force kill if still running
        if ps -p $PID > /dev/null; then
            kill -9 $PID
        fi
        rm /tmp/hosp_gunicorn.pid
        echo "✓ Process stopped"
    else
        echo "⚠ PID file exists but process not running"
        rm /tmp/hosp_gunicorn.pid
    fi
fi

# Kill any remaining gunicorn processes for this app
if pgrep -f "gunicorn.*diagcenter" > /dev/null; then
    echo "→ Cleaning up remaining processes..."
    sudo pkill -f "gunicorn.*diagcenter"
    echo "✓ Cleanup complete"
fi

# Kill any process on port 8005
if lsof -Pi :8005 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "→ Freeing port 8005..."
    sudo kill -9 $(lsof -t -i:8005) 2>/dev/null
    echo "✓ Port 8005 freed"
fi

echo ""
echo "✓ Hospital System stopped"
