#!/bin/bash
# ============================================
# Deploy Flask Backend Script
# ============================================

set -e

echo "============================================"
echo "🔧 Deploying Flask Backend..."
echo "============================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DEST="/var/www/backend"

echo "Source: $REPO_DIR"
echo "Destination: $BACKEND_DEST"

echo ""
echo "Step 1: Copying backend files..."
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='.git' --exclude='*.pyc' --exclude='deploy' \
    "$REPO_DIR/" "$BACKEND_DEST/"

# Also copy deploy folder for future updates
mkdir -p "$BACKEND_DEST/deploy"
cp "$SCRIPT_DIR"/*.sh "$BACKEND_DEST/deploy/" 2>/dev/null || true

echo ""
echo "Step 2: Creating Python virtual environment..."
cd "$BACKEND_DEST"
python3.11 -m venv venv
source venv/bin/activate

echo ""
echo "Step 3: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn gevent

echo ""
echo "Step 4: Setting up production environment..."
if [ ! -f "$BACKEND_DEST/.env" ]; then
    cat > "$BACKEND_DEST/.env" << 'EOF'
# ================================
# PRODUCTION ENVIRONMENT - AWS
# ================================

# Database - MongoDB Atlas (REQUIRED)
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/worlds_ai_bot

# JWT Secret - CHANGE THIS! Generate with: python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET=your-production-secret-key-change-me

# ================================
# IMPORTANT: Your Vercel Frontend URL
# ================================
# Add your Vercel deployment URL here (without trailing slash)
FRONTEND_URL=https://your-app.vercel.app

# CORS
CORS_CREDENTIALS=true

# Email Configuration
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

# Razorpay (use live keys)
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_live_secret

# Production settings
FLASK_ENV=production
PORT=5000
EOF
    echo -e "${YELLOW}[!]${NC} Created .env file"
    echo "    IMPORTANT: Update with your values!"
    echo "    Run: sudo nano $BACKEND_DEST/.env"
fi

echo ""
echo "Step 5: Setting permissions..."
chown -R ec2-user:ec2-user "$BACKEND_DEST"
chmod 600 "$BACKEND_DEST/.env"

echo ""
echo "Step 6: Restarting services..."
sudo systemctl restart worldsaibot-backend
sudo systemctl restart nginx

echo ""
echo "Step 7: Checking status..."
sleep 2
if systemctl is-active --quiet worldsaibot-backend; then
    echo -e "${GREEN}[✓]${NC} Backend service is running"
else
    echo -e "${YELLOW}[!]${NC} Backend service may have issues. Check logs:"
    echo "    sudo journalctl -u worldsaibot-backend -n 20"
fi

echo ""
echo "============================================"
echo -e "${GREEN}🎉 Backend Deployment Complete!${NC}"
echo "============================================"
echo ""
echo "Your API is now available at:"
echo "  http://YOUR_EC2_PUBLIC_IP"
echo ""
echo "IMPORTANT - Update your .env file:"
echo "  sudo nano /var/www/backend/.env"
echo ""
echo "Set these values:"
echo "  - DATABASE_URL: Your MongoDB Atlas connection string"
echo "  - JWT_SECRET: A strong random secret"
echo "  - FRONTEND_URL: Your Vercel frontend URL (e.g., https://your-app.vercel.app)"
echo ""
echo "Then restart: sudo systemctl restart worldsaibot-backend"
echo ""
