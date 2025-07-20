# 🏭 Production Deployment Guide

## 📋 Pre-deployment Checklist

- [ ] Ubuntu Server 20.04+ tersedia
- [ ] SSH access ke server
- [ ] Domain/IP address ready
- [ ] Firewall rules configured

## 🚀 Quick Deploy to Ubuntu Server

### Option 1: Automatic Setup Script

```bash
# 1. Upload project ke server
scp -r pegadaian-project/ ubuntu@your-server-ip:/opt/

# 2. SSH ke server
ssh ubuntu@your-server-ip

# 3. Jalankan setup
cd /opt/pegadaian-project
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### Option 2: Using Deploy Script

```bash
# Dari local machine
./deploy.sh your-server-ip ubuntu
```

## 🔧 Manual Production Setup

### 1. System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv \
                    google-chrome-stable \
                    xvfb \
                    nginx \
                    supervisor
```

### 2. Application Setup

```bash
# Create app directory
sudo mkdir -p /opt/pegadaian-scraper
sudo chown $USER:$USER /opt/pegadaian-scraper
cd /opt/pegadaian-scraper

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_clean.txt

# Create data directory
mkdir -p data logs
```

### 3. Environment Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit configuration
nano .env
```

### 4. Systemd Service

```bash
# Service sudah dibuat oleh setup script
sudo systemctl enable pegadaian-api
sudo systemctl start pegadaian-api
sudo systemctl status pegadaian-api
```

### 5. Nginx Reverse Proxy (Optional)

```bash
sudo nano /etc/nginx/sites-available/pegadaian-api
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/pegadaian-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 📊 Monitoring & Maintenance

### System Health

```bash
# Check service status
sudo systemctl status pegadaian-api

# View logs
sudo journalctl -u pegadaian-api -f

# Check system resources
htop
df -h
free -h
```

### Application Logs

```bash
# API logs
tail -f /opt/pegadaian-scraper/logs/api.log

# Scraper logs
tail -f /opt/pegadaian-scraper/logs/scraper.log
```

### Performance Monitoring

```bash
# Monitor API endpoints
curl http://localhost:8001/health

# Check Chrome processes
ps aux | grep chrome

# Monitor data directory
ls -la /opt/pegadaian-scraper/data/
```

## 🔄 Updates & Deployment

### Update Application

```bash
cd /opt/pegadaian-scraper
git pull origin main  # jika menggunakan git
# atau copy files baru

source venv/bin/activate
pip install -r requirements_clean.txt

sudo systemctl restart pegadaian-api
```

### Rolling Back

```bash
sudo systemctl stop pegadaian-api
# restore previous version
sudo systemctl start pegadaian-api
```

## 🔐 Security Considerations

### Firewall Setup

```bash
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8001/tcp  # if accessing directly
sudo ufw enable
```

### SSL Certificate (with Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Process Security

```bash
# Run as non-root user
sudo useradd -r -s /bin/false pegadaian
sudo chown -R pegadaian:pegadaian /opt/pegadaian-scraper
```

## 🚨 Troubleshooting

### Common Issues

**Chrome/ChromeDriver mismatch:**
```bash
google-chrome --version
chromedriver --version
# Reinstall ChromeDriver if versions don't match
```

**Memory issues:**
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Permission issues:**
```bash
sudo chown -R $USER:$USER /opt/pegadaian-scraper
chmod +x setup_ubuntu.sh run_api.sh
```

**API not responding:**
```bash
sudo systemctl restart pegadaian-api
sudo journalctl -u pegadaian-api --since "5 minutes ago"
```

## 📈 Performance Optimization

### Production Settings

```bash
# Use production ASGI server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
         --bind 0.0.0.0:8001 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log
```

### Caching Strategy

- Enable Redis for caching scraped data
- Set appropriate cache TTL
- Implement rate limiting

### Resource Limits

```bash
# Set system limits
echo "pegadaian soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "pegadaian hard nofile 65536" | sudo tee -a /etc/security/limits.conf
```

## 🔄 Backup Strategy

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/opt/backups/pegadaian"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/pegadaian_backup_$DATE.tar.gz \
    /opt/pegadaian-scraper/data/ \
    /opt/pegadaian-scraper/.env

# Keep only last 7 days
find $BACKUP_DIR -name "pegadaian_backup_*.tar.gz" -mtime +7 -delete
```
