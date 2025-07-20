#!/bin/bash

# Script untuk menjalankan API di Ubuntu Server
# Usage: ./run_api.sh [port]

PORT=${1:-8001}
HOST="0.0.0.0"

echo "🚀 Starting Pegadaian Scraper API..."
echo "📍 Host: $HOST"
echo "🔌 Port: $PORT"
echo "🌐 URL: http://localhost:$PORT"
echo ""

# Aktivasi virtual environment jika ada
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Set display untuk headless Chrome
export DISPLAY=:99

# Start Xvfb jika belum running (untuk headless Chrome)
if ! pgrep Xvfb > /dev/null; then
    echo "🖥️  Starting virtual display..."
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    sleep 2
fi

# Jalankan API
echo "🔄 Starting API server..."
python -m uvicorn main:app --host $HOST --port $PORT --reload

echo "❌ API server stopped."
