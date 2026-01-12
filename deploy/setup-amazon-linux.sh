#!/bin/bash
# ============================================
# Amazon Linux 2023 Setup Script
# Worlds AI Bot - Backend Only Deployment
# ============================================

set -e

echo "============================================"
echo "🚀 Worlds AI Bot Backend - AWS Setup"
echo "============================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script with sudo"
    exit 1
fi

echo ""
echo "Step 1: Updating system packages..."
dnf update -y
print_status "System updated"

echo ""
echo "Step 2: Installing essential packages..."
dnf install -y git curl wget vim nano htop unzip tar
dnf groupinstall -y "Development Tools"
print_status "Essential packages installed"

echo ""
echo "Step 3: Installing Python 3.11..."
dnf install -y python3.11 python3.11-pip python3.11-devel
if [ ! -f /usr/bin/python3 ]; then
    ln -s /usr/bin/python3.11 /usr/bin/python3
fi
python3.11 --version
print_status "Python 3.11 installed"

echo ""
echo "Step 4: Installing Nginx..."
dnf install -y nginx
systemctl enable nginx
print_status "Nginx installed"

echo ""
echo "Step 5: Creating application directories..."
mkdir -p /var/www/backend
mkdir -p /var/log/worldsaibot
chown -R ec2-user:ec2-user /var/www
chown -R ec2-user:ec2-user /var/log/worldsaibot
print_status "Directories created"

echo ""
echo "Step 6: Installing Gunicorn..."
pip3.11 install gunicorn gevent
print_status "Gunicorn installed"

echo ""
echo "Step 7: Setting up systemd service..."
cat > /etc/systemd/system/worldsaibot-backend.service << 'EOF'
[Unit]
Description=Worlds AI Bot Flask Backend
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/var/www/backend
Environment="PATH=/var/www/backend/venv/bin"
EnvironmentFile=/var/www/backend/.env
ExecStart=/var/www/backend/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 --access-logfile /var/log/worldsaibot/access.log --error-logfile /var/log/worldsaibot/error.log app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
print_status "Systemd service configured"

echo ""
echo "Step 8: Configuring Nginx for API..."
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup 2>/dev/null || true

cat > /etc/nginx/nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent"';
    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 4096;
    client_max_body_size 50M;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain application/json application/javascript text/css;

    include /etc/nginx/conf.d/*.conf;
}
EOF

cat > /etc/nginx/conf.d/backend-api.conf << 'EOF'
upstream flask_backend {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name _;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    # CORS headers for API
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, PATCH, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Requested-With" always;
    add_header Access-Control-Allow-Credentials "true" always;

    # Handle preflight OPTIONS requests
    if ($request_method = OPTIONS) {
        return 204;
    }

    # Proxy all requests to Flask
    location / {
        proxy_pass http://flask_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
EOF

nginx -t
print_status "Nginx configured"

echo ""
echo "Step 9: Setting up log rotation..."
cat > /etc/logrotate.d/worldsaibot << 'EOF'
/var/log/worldsaibot/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ec2-user ec2-user
}
EOF
print_status "Log rotation configured"

echo ""
echo "============================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Clone your backend repo:"
echo "     git clone https://github.com/YOUR_USERNAME/worlds_ai_bot_flask_backend.git"
echo ""
echo "  2. Run the deploy script:"
echo "     cd worlds_ai_bot_flask_backend/deploy"
echo "     ./deploy.sh"
echo ""
echo "  3. Update .env with your Vercel frontend URL:"
echo "     sudo nano /var/www/backend/.env"
echo "     Set: FRONTEND_URL=https://your-app.vercel.app"
echo ""
