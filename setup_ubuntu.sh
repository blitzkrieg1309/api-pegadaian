#!/bin/bash

# Script setup untuk Ubuntu Server
# Menjalankan: chmod +x setup_ubuntu.sh && ./setup_ubuntu.sh

echo "🚀 Setting up Pegadaian Scraper API on Ubuntu Server..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 dan pip jika belum ada
echo "🐍 Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome untuk Selenium
echo "🌐 Installing Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver
echo "🔧 Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f3 | cut -d '.' -f1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")
wget -N "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Install system dependencies
echo "📚 Installing system dependencies..."
sudo apt install -y wget curl unzip xvfb

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment dan install requirements
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/pegadaian-api.service > /dev/null <<EOF
[Unit]
Description=Pegadaian Scraper API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable dan start service
sudo systemctl daemon-reload
sudo systemctl enable pegadaian-api.service

echo "✅ Setup completed!"
echo ""
echo "🔧 To start the API service:"
echo "sudo systemctl start pegadaian-api"
echo ""
echo "📊 To check service status:"
echo "sudo systemctl status pegadaian-api"
echo ""
echo "📝 To view logs:"
echo "sudo journalctl -u pegadaian-api -f"
echo ""
echo "🌐 API will be available at: http://your-server-ip:8001"
