# 🚀 AWS Deployment Guide - Backend API

Deploy the Flask backend on Amazon Linux 2023 EC2.

## 📋 Prerequisites

- Amazon Linux 2023 EC2 instance (t2.micro or larger)
- MongoDB Atlas account
- Your Vercel frontend URL

## 🔧 Quick Deployment

### Step 1: Connect to EC2
```bash
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP
```

### Step 2: Run setup script (first time only)
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/worlds_ai_bot_flask_backend.git
cd worlds_ai_bot_flask_backend/deploy

# Run setup
chmod +x *.sh
sudo ./setup-amazon-linux.sh
```

### Step 3: Deploy the backend
```bash
./deploy.sh
```

### Step 4: Configure environment variables
```bash
sudo nano /var/www/backend/.env
```

**IMPORTANT:** Set these values:
```env
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/worlds_ai_bot
JWT_SECRET=your-strong-secret-key
FRONTEND_URL=https://your-app.vercel.app
```

### Step 5: Restart the service
```bash
sudo systemctl restart worldsaibot-backend
```

## 🔗 Connecting Frontend & Backend

### On AWS (Backend):
Set `FRONTEND_URL` in `/var/www/backend/.env`:
```env
FRONTEND_URL=https://your-app.vercel.app
```

### On Vercel (Frontend):
Add environment variable in Vercel Dashboard:
```
VITE_BACKEND_URL=http://YOUR_EC2_PUBLIC_IP
```
Or if using a domain:
```
VITE_BACKEND_URL=https://api.yourdomain.com
```

## 📝 Useful Commands

```bash
# Check status
sudo systemctl status worldsaibot-backend

# View logs
sudo journalctl -u worldsaibot-backend -f

# Restart
sudo systemctl restart worldsaibot-backend

# Test API
curl http://localhost:5000/
```

## 🔒 SSL Setup (Recommended)

If you have a domain:
```bash
sudo dnf install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

## 🔄 Updating

```bash
cd ~/worlds_ai_bot_flask_backend
git pull
cd deploy
./deploy.sh
```
