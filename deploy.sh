#!/bin/bash

# Script deploy ke Ubuntu Server
# Usage: ./deploy.sh [server_ip] [username]

set -e

SERVER_IP=${1:-"your-server-ip"}
USERNAME=${2:-"ubuntu"}
PROJECT_DIR="/opt/pegadaian-scraper"

echo "🚀 Deploying Pegadaian Scraper API to Ubuntu Server..."
echo "📍 Server: $USERNAME@$SERVER_IP"
echo "📁 Remote directory: $PROJECT_DIR"
echo ""

# Fungsi untuk eksekusi remote command
remote_exec() {
    ssh $USERNAME@$SERVER_IP "$1"
}

# Fungsi untuk copy file
copy_files() {
    rsync -avz --exclude='venv' --exclude='data' --exclude='__pycache__' \
          --exclude='.git' --exclude='*.log' \
          ./ $USERNAME@$SERVER_IP:$PROJECT_DIR/
}

echo "📦 Copying files to server..."
remote_exec "sudo mkdir -p $PROJECT_DIR && sudo chown $USERNAME:$USERNAME $PROJECT_DIR"
copy_files

echo "🔧 Setting up environment on server..."
remote_exec "cd $PROJECT_DIR && chmod +x setup_ubuntu.sh run_api.sh"

echo "📚 Installing dependencies..."
remote_exec "cd $PROJECT_DIR && ./setup_ubuntu.sh"

echo "🔄 Restarting service..."
remote_exec "sudo systemctl restart pegadaian-api"

echo "✅ Deployment completed!"
echo ""
echo "🔧 Useful commands:"
echo "ssh $USERNAME@$SERVER_IP 'sudo systemctl status pegadaian-api'"
echo "ssh $USERNAME@$SERVER_IP 'sudo journalctl -u pegadaian-api -f'"
echo ""
echo "🌐 API should be available at: http://$SERVER_IP:8001"
