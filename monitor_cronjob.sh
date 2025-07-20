#!/bin/bash

# Script untuk monitoring auto scraping cronjob
# Usage: ./monitor_cronjob.sh [command]

PROJECT_DIR="/home/alfatih1309/project/api-pegadaian"
LOG_FILE="$PROJECT_DIR/logs/auto_scrape.log"
API_URL="http://localhost:8001"

# Function to show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  status    - Show cronjob status and recent logs"
    echo "  logs      - Show recent scraping logs"
    echo "  test      - Test manual scraping"
    echo "  enable    - Enable cronjob"
    echo "  disable   - Disable cronjob"
    echo "  remove    - Remove cronjob completely"
    echo "  api       - Check API status"
    echo ""
}

# Function to check API status
check_api_status() {
    echo "🔍 Checking API status..."
    
    # Health check
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" --connect-timeout 5)
    if [ "$response" = "200" ]; then
        echo "✅ API is healthy (HTTP $response)"
        
        # Get cache info
        cache_info=$(curl -s "$API_URL/cache-info" --connect-timeout 5)
        echo "💾 Cache info: $cache_info"
        
        # Get last scraping data
        last_data=$(curl -s "$API_URL/gold-prices" --connect-timeout 5 | head -c 200)
        echo "📊 Last data: ${last_data}..."
    else
        echo "❌ API is not responding (HTTP $response)"
        echo "🔧 Try: sudo systemctl restart pegadaian-api"
    fi
}

# Function to show cronjob status
show_status() {
    echo "📋 Cronjob Status:"
    
    if crontab -l 2>/dev/null | grep -q "auto_scrape.sh"; then
        echo "✅ Cronjob is installed"
        echo "📅 Schedule: $(crontab -l | grep auto_scrape.sh | awk '{print $1, $2, $3, $4, $5}')"
        
        # Check if log file exists and show recent entries
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "📝 Recent log entries (last 10 lines):"
            tail -n 10 "$LOG_FILE"
            
            echo ""
            echo "📊 Scraping statistics (last 24 hours):"
            grep "$(date '+%Y-%m-%d')" "$LOG_FILE" | grep -c "SUCCESS" | xargs echo "Successful runs:"
            grep "$(date '+%Y-%m-%d')" "$LOG_FILE" | grep -c "ERROR" | xargs echo "Failed runs:"
        else
            echo "⚠️  No log file found yet"
        fi
    else
        echo "❌ Cronjob is not installed"
        echo "🔧 Run: ./setup_cronjob.sh"
    fi
}

# Function to show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo "📖 Showing scraping logs (press Ctrl+C to exit):"
        tail -f "$LOG_FILE"
    else
        echo "❌ No log file found: $LOG_FILE"
    fi
}

# Function to test manual scraping
test_scraping() {
    echo "🧪 Testing manual scraping..."
    echo "⏳ This may take 30-60 seconds..."
    
    response=$(curl -X POST "$API_URL/scrape" \
                    -H "Content-Type: application/json" \
                    --connect-timeout 30 \
                    --max-time 120 \
                    -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n")
    
    if [ $? -eq 0 ]; then
        echo "✅ Manual scraping completed successfully"
        echo "Response: $response"
    else
        echo "❌ Manual scraping failed"
    fi
}

# Function to enable cronjob
enable_cronjob() {
    if crontab -l 2>/dev/null | grep -q "auto_scrape.sh"; then
        # Uncomment if commented
        crontab -l | sed 's/^#.*auto_scrape.sh/0 * * * * \/home\/alfatih1309\/project\/api-pegadaian\/auto_scrape.sh/' | crontab -
        echo "✅ Cronjob enabled"
    else
        echo "❌ Cronjob not found. Run ./setup_cronjob.sh first"
    fi
}

# Function to disable cronjob
disable_cronjob() {
    if crontab -l 2>/dev/null | grep -q "auto_scrape.sh"; then
        # Comment out the cronjob
        crontab -l | sed 's/^.*auto_scrape.sh/#&/' | crontab -
        echo "✅ Cronjob disabled (commented out)"
    else
        echo "❌ Cronjob not found"
    fi
}

# Function to remove cronjob
remove_cronjob() {
    if crontab -l 2>/dev/null | grep -q "auto_scrape.sh"; then
        crontab -l | grep -v "auto_scrape.sh" | crontab -
        echo "✅ Cronjob removed completely"
    else
        echo "❌ Cronjob not found"
    fi
}

# Main script
case "$1" in
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "test")
        test_scraping
        ;;
    "enable")
        enable_cronjob
        ;;
    "disable")
        disable_cronjob
        ;;
    "remove")
        remove_cronjob
        ;;
    "api")
        check_api_status
        ;;
    *)
        show_usage
        ;;
esac
