#!/bin/bash

# Script untuk setup cronjob auto scraping
# Usage: ./setup_cronjob.sh

PROJECT_DIR="/home/alfatih1309/project/api-pegadaian"
SCRIPT_PATH="$PROJECT_DIR/auto_scrape.sh"
LOG_DIR="$PROJECT_DIR/logs"

echo "🕐 Setting up Auto Scraping Cronjob..."

# Create logs directory
mkdir -p "$LOG_DIR"

# Make auto_scrape.sh executable
chmod +x "$SCRIPT_PATH"

# Check if cronjob already exists
if crontab -l 2>/dev/null | grep -q "auto_scrape.sh"; then
    echo "⚠️  Cronjob already exists. Removing old one..."
    crontab -l 2>/dev/null | grep -v "auto_scrape.sh" | crontab -
fi

# Add new cronjob (every hour at minute 0)
echo "📅 Adding cronjob to run every hour..."
(crontab -l 2>/dev/null; echo "0 * * * * $SCRIPT_PATH") | crontab -

# Verify cronjob was added
echo "✅ Cronjob setup complete!"
echo ""
echo "📋 Current crontab:"
crontab -l

echo ""
echo "🔧 Useful commands:"
echo "View cronjob logs: tail -f $LOG_DIR/auto_scrape.log"
echo "Check crontab: crontab -l"
echo "Edit crontab: crontab -e"
echo "Remove cronjob: crontab -l | grep -v 'auto_scrape.sh' | crontab -"
echo ""
echo "📊 Test cronjob manually:"
echo "$SCRIPT_PATH"
echo ""
echo "⏰ Cronjob schedule: Every hour at minute 0"
echo "Next run times:"
echo "$(date -d '+1 hour' '+%Y-%m-%d %H:00:00')"
echo "$(date -d '+2 hour' '+%Y-%m-%d %H:00:00')"
echo "$(date -d '+3 hour' '+%Y-%m-%d %H:00:00')"
