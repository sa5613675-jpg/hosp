#!/bin/bash

# Production Deployment Script for Ubuntu VPS
# Universal Health Services And Diagnostic Center

echo "======================================================================================================"
echo "                  PRODUCTION DEPLOYMENT - UBUNTU VPS"
echo "======================================================================================================"
echo "Hospital: Universal Health Services And Diagnostic Center"
echo "======================================================================================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/var/www/diagcenter"
APP_USER="www-data"
VENV_PATH="$APP_DIR/venv"
PYTHON="$VENV_PATH/bin/python"
PIP="$VENV_PATH/bin/pip"
GUNICORN="$VENV_PATH/bin/gunicorn"

echo ""
echo -e "${YELLOW}Step 1: Updating system packages${NC}"
sudo apt update
sudo apt upgrade -y

echo ""
echo -e "${YELLOW}Step 2: Installing required packages${NC}"
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y nginx supervisor
sudo apt install -y postgresql postgresql-contrib libpq-dev
sudo apt install -y git curl wget

echo ""
echo -e "${YELLOW}Step 3: Creating application directory${NC}"
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR

echo ""
echo -e "${YELLOW}Step 4: Cloning/Updating application code${NC}"
if [ -d "$APP_DIR/.git" ]; then
    echo "Updating existing repository..."
    cd $APP_DIR
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/mahindx0-crypto/hosp.git $APP_DIR
    cd $APP_DIR
fi

echo ""
echo -e "${YELLOW}Step 5: Setting up Python virtual environment${NC}"
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv $VENV_PATH
fi
source $VENV_PATH/bin/activate

echo ""
echo -e "${YELLOW}Step 6: Installing Python dependencies${NC}"
$PIP install --upgrade pip
$PIP install -r requirements.txt
$PIP install gunicorn psycopg2-binary

echo ""
echo -e "${YELLOW}Step 7: Configuring database${NC}"
echo "Note: Make sure PostgreSQL is configured with your database credentials"
echo "Default database: diagcenter_db"
echo "Update diagcenter/settings.py with your database settings"

echo ""
echo -e "${YELLOW}Step 8: Running Django migrations${NC}"
$PYTHON manage.py makemigrations
$PYTHON manage.py migrate

echo ""
echo -e "${YELLOW}Step 9: Collecting static files${NC}"
$PYTHON manage.py collectstatic --noinput

echo ""
echo -e "${YELLOW}Step 10: Setting up Gunicorn${NC}"
cat > $APP_DIR/gunicorn_config.py << 'EOF'
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/var/log/diagcenter/gunicorn_access.log"
errorlog = "/var/log/diagcenter/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "diagcenter"

# Server mechanics
daemon = False
pidfile = "/var/run/diagcenter/gunicorn.pid"
user = "www-data"
group = "www-data"

# SSL
# keyfile = "/path/to/ssl/key.pem"
# certfile = "/path/to/ssl/cert.pem"
EOF

# Create log and run directories
sudo mkdir -p /var/log/diagcenter
sudo mkdir -p /var/run/diagcenter
sudo chown -R www-data:www-data /var/log/diagcenter
sudo chown -R www-data:www-data /var/run/diagcenter

echo ""
echo -e "${YELLOW}Step 11: Configuring Supervisor${NC}"
sudo tee /etc/supervisor/conf.d/diagcenter.conf > /dev/null << EOF
[program:diagcenter]
directory=$APP_DIR
command=$GUNICORN diagcenter.wsgi:application -c $APP_DIR/gunicorn_config.py
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/diagcenter/supervisor.log
stderr_logfile=/var/log/diagcenter/supervisor_error.log
environment=PATH="$VENV_PATH/bin"
EOF

echo ""
echo -e "${YELLOW}Step 12: Configuring Nginx${NC}"
sudo tee /etc/nginx/sites-available/diagcenter > /dev/null << 'EOF'
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;
    
    client_max_body_size 100M;
    
    # Static files
    location /static/ {
        alias /var/www/diagcenter/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/diagcenter/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/diagcenter /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo ""
echo -e "${YELLOW}Step 13: Setting file permissions${NC}"
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/media
sudo chmod 664 $APP_DIR/db.sqlite3 2>/dev/null || true

echo ""
echo -e "${YELLOW}Step 14: Restarting services${NC}"
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart diagcenter
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
sudo systemctl enable supervisor

echo ""
echo "======================================================================================================"
echo -e "${GREEN}✓ PRODUCTION DEPLOYMENT COMPLETE!${NC}"
echo "======================================================================================================"
echo ""
echo "Next steps:"
echo "1. Update diagcenter/settings.py:"
echo "   - Set DEBUG = False"
echo "   - Add your domain to ALLOWED_HOSTS"
echo "   - Configure PostgreSQL database"
echo "   - Set SECRET_KEY to a strong random value"
echo ""
echo "2. Update Nginx config:"
echo "   - Replace 'your_domain.com' with your actual domain"
echo "   sudo nano /etc/nginx/sites-available/diagcenter"
echo ""
echo "3. Setup SSL certificate (recommended):"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d your_domain.com"
echo ""
echo "4. Monitor logs:"
echo "   Gunicorn: tail -f /var/log/diagcenter/gunicorn_error.log"
echo "   Supervisor: tail -f /var/log/diagcenter/supervisor.log"
echo "   Nginx: tail -f /var/log/nginx/error.log"
echo ""
echo "5. Manage application:"
echo "   sudo supervisorctl status diagcenter"
echo "   sudo supervisorctl restart diagcenter"
echo "   sudo systemctl restart nginx"
echo ""
echo "======================================================================================================"
