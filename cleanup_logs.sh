#!/bin/bash

# Script untuk cleanup log files auto scraping
# Usage: ./cleanup_logs.sh [days]

PROJECT_DIR="/home/alfatih1309/project/api-pegadaian"
LOG_DIR="$PROJECT_DIR/logs"
DEFAULT_DAYS=7

# Get number of days from parameter or use default
DAYS=${1:-$DEFAULT_DAYS}

echo "🧹 Log Cleanup Script"
echo "📁 Log directory: $LOG_DIR"
echo "📅 Keeping logs from last $DAYS days"
echo ""

# Create logs directory if not exists
mkdir -p "$LOG_DIR"

# Function to clean log files
cleanup_logs() {
    local log_file="$LOG_DIR/auto_scrape.log"
    local backup_file="$LOG_DIR/auto_scrape_$(date '+%Y%m%d_%H%M%S').log.bak"
    
    if [ -f "$log_file" ]; then
        echo "📊 Current log file size: $(du -h "$log_file" | cut -f1)"
        echo "📝 Current log lines: $(wc -l < "$log_file")"
        
        # Create backup of current log
        cp "$log_file" "$backup_file"
        echo "💾 Backup created: $backup_file"
        
        # Keep only logs from last N days
        local cutoff_date=$(date -d "$DAYS days ago" '+%Y-%m-%d')
        echo "🗓️  Keeping logs from: $cutoff_date onwards"
        
        # Filter log file
        awk -v cutoff="$cutoff_date" '
        {
            if (match($0, /[0-9]{4}-[0-9]{2}-[0-9]{2}/)) {
                log_date = substr($0, RSTART, RLENGTH)
                if (log_date >= cutoff) {
                    print $0
                }
            }
        }' "$log_file" > "${log_file}.tmp"
        
        # Replace original with filtered content
        mv "${log_file}.tmp" "$log_file"
        
        echo "✅ Log cleanup completed"
        echo "📊 New log file size: $(du -h "$log_file" | cut -f1)"
        echo "📝 New log lines: $(wc -l < "$log_file")"
    else
        echo "⚠️  No log file found: $log_file"
    fi
}

# Function to clean old backup files
cleanup_backups() {
    echo ""
    echo "🗂️  Cleaning old backup files..."
    
    # Remove backup files older than 30 days
    find "$LOG_DIR" -name "*.log.bak" -type f -mtime +30 -delete
    
    # Show remaining backups
    local backup_count=$(find "$LOG_DIR" -name "*.log.bak" -type f | wc -l)
    echo "📦 Remaining backup files: $backup_count"
    
    if [ $backup_count -gt 0 ]; then
        echo "📋 Backup files:"
        find "$LOG_DIR" -name "*.log.bak" -type f -exec ls -lh {} \;
    fi
}

# Function to show disk usage
show_disk_usage() {
    echo ""
    echo "💾 Disk usage in logs directory:"
    du -sh "$LOG_DIR"/* 2>/dev/null || echo "No files found"
    
    echo ""
    echo "💿 Available disk space:"
    df -h "$PROJECT_DIR" | tail -1
}

# Validate days parameter
if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ]; then
    echo "❌ Error: Days must be a positive number"
    echo "Usage: $0 [days]"
    echo "Example: $0 7  (keep last 7 days)"
    exit 1
fi

# Run cleanup
cleanup_logs
cleanup_backups
show_disk_usage

echo ""
echo "✨ Cleanup completed!"
echo ""
echo "💡 To automate log cleanup, add this to crontab:"
echo "   0 2 * * 0 $PROJECT_DIR/cleanup_logs.sh 7"
echo "   (runs every Sunday at 2 AM, keeps 7 days of logs)"
