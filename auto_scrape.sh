#!/bin/bash

# Auto Scraping Script untuk Cronjob
# Script ini akan memanggil endpoint /scrape setiap jam

# Configuration
API_URL="http://localhost:8001"
LOG_DIR="/home/alfatih1309/project/api-pegadaian/logs"
LOG_FILE="$LOG_DIR/auto_scrape.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create log directory if not exists
mkdir -p "$LOG_DIR"

# Function to log messages
log_message() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Function to check if API is running
check_api_health() {
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" --connect-timeout 10)
    if [ "$response" = "200" ]; then
        return 0
    else
        return 1
    fi
}

# Function to trigger scraping
trigger_scrape() {
    response=$(curl -s -X POST "$API_URL/scrape" \
                    -H "Content-Type: application/json" \
                    --connect-timeout 30 \
                    --max-time 120)
    
    if [ $? -eq 0 ]; then
        log_message "SUCCESS: Scraping completed successfully"
        log_message "Response: $response"
        return 0
    else
        log_message "ERROR: Failed to trigger scraping"
        return 1
    fi
}

# Main execution
log_message "=== AUTO SCRAPE JOB STARTED ==="

# Check if API is healthy
if check_api_health; then
    log_message "API health check: OK"
    
    # Trigger scraping
    if trigger_scrape; then
        log_message "Auto scraping job completed successfully"
    else
        log_message "Auto scraping job failed"
        # Try to restart service if scraping fails
        log_message "Attempting to restart pegadaian-api service..."
        sudo systemctl restart pegadaian-api
        sleep 10
        
        # Try scraping again after restart
        if check_api_health && trigger_scrape; then
            log_message "Scraping successful after service restart"
        else
            log_message "Scraping still failed after service restart"
        fi
    fi
else
    log_message "ERROR: API health check failed - service may be down"
    log_message "Attempting to restart pegadaian-api service..."
    sudo systemctl restart pegadaian-api
    sleep 15
    
    # Check again after restart
    if check_api_health; then
        log_message "Service restarted successfully, triggering scrape..."
        trigger_scrape
    else
        log_message "ERROR: Service restart failed"
    fi
fi

log_message "=== AUTO SCRAPE JOB ENDED ==="
log_message ""
