# Automated Scraping with Cronjob

This document explains how to set up and manage automated scraping using cronjob for the Pegadaian API project.

## Overview

The automated scraping system runs every hour and includes:
- 🕐 Hourly data collection (runs at minute 0 of every hour)
- 🔍 Health checks before scraping
- 🚀 Automatic service restart on failures
- 📝 Comprehensive logging
- 🧹 Log rotation and cleanup

## Setup Scripts

### 1. `auto_scrape.sh`
Main automation script that:
- Checks API health
- Triggers scraping via API endpoint
- Handles timeouts and errors
- Restarts service if needed
- Logs all activities

### 2. `setup_cronjob.sh`
Installation script that:
- Sets up the cronjob schedule
- Creates necessary directories
- Sets proper permissions
- Verifies installation

### 3. `monitor_cronjob.sh`
Management and monitoring script with commands:
- `status` - Show cronjob status and recent logs
- `logs` - Show real-time log monitoring
- `test` - Test manual scraping
- `enable/disable` - Control cronjob execution
- `remove` - Remove cronjob completely
- `api` - Check API health

### 4. `cleanup_logs.sh`
Log maintenance script that:
- Cleans old log entries
- Creates backups
- Manages disk space
- Shows usage statistics

## Installation

1. **Upload scripts to server:**
```bash
scp auto_scrape.sh setup_cronjob.sh monitor_cronjob.sh cleanup_logs.sh username@server:/home/alfatih1309/project/api-pegadaian/
```

2. **Make scripts executable:**
```bash
chmod +x auto_scrape.sh setup_cronjob.sh monitor_cronjob.sh cleanup_logs.sh
```

3. **Run setup:**
```bash
./setup_cronjob.sh
```

## Usage

### Check Status
```bash
./monitor_cronjob.sh status
```

### View Real-time Logs
```bash
./monitor_cronjob.sh logs
```

### Test Manual Scraping
```bash
./monitor_cronjob.sh test
```

### Control Cronjob
```bash
# Disable temporarily
./monitor_cronjob.sh disable

# Enable again
./monitor_cronjob.sh enable

# Remove completely
./monitor_cronjob.sh remove
```

### Check API Health
```bash
./monitor_cronjob.sh api
```

### Clean Old Logs
```bash
# Keep last 7 days
./cleanup_logs.sh 7

# Keep last 30 days
./cleanup_logs.sh 30
```

## Cronjob Schedule

The default schedule is: `0 * * * *` (every hour at minute 0)

To modify the schedule:
1. Edit crontab: `crontab -e`
2. Update the time pattern:
   - `0 */2 * * *` - Every 2 hours
   - `0 8,20 * * *` - At 8 AM and 8 PM daily
   - `0 9-17 * * 1-5` - Every hour from 9 AM to 5 PM, Monday to Friday

## Log Files

### Main Log: `/home/alfatih1309/project/api-pegadaian/logs/auto_scrape.log`

Log format:
```
[2024-01-15 14:00:01] Starting auto scrape...
[2024-01-15 14:00:02] SUCCESS: API health check passed
[2024-01-15 14:00:45] SUCCESS: Scraping completed in 43.2 seconds
[2024-01-15 14:00:45] Auto scrape finished successfully
```

### Log Levels:
- `SUCCESS` - Operation completed successfully
- `ERROR` - Operation failed
- `WARNING` - Non-critical issues
- `INFO` - General information

## Monitoring

### Check if cronjob is running:
```bash
# View crontab
crontab -l

# Check cron service
sudo systemctl status cron

# View cron logs
grep auto_scrape /var/log/syslog
```

### Performance Monitoring:
```bash
# Check API response time
curl -w "Time: %{time_total}s\n" http://localhost:8001/health

# Check system resources
htop

# Check disk space
df -h
```

## Troubleshooting

### Common Issues:

1. **Cronjob not running:**
   ```bash
   # Check cron service
   sudo systemctl status cron
   
   # Restart if needed
   sudo systemctl restart cron
   ```

2. **API not responding:**
   ```bash
   # Check service status
   sudo systemctl status pegadaian-api
   
   # Restart service
   sudo systemctl restart pegadaian-api
   ```

3. **Scraping timeouts:**
   - Check server resources
   - Verify Chrome/ChromeDriver installation
   - Check network connectivity

4. **Permission errors:**
   ```bash
   # Fix script permissions
   chmod +x *.sh
   
   # Fix log directory permissions
   chmod 755 logs/
   ```

### Log Analysis:
```bash
# Count successful runs today
grep "$(date '+%Y-%m-%d')" logs/auto_scrape.log | grep -c "SUCCESS"

# Check for errors
grep "ERROR" logs/auto_scrape.log | tail -10

# View scraping performance
grep "completed in" logs/auto_scrape.log | tail -5
```

## Automated Log Cleanup

To automatically clean logs weekly:
```bash
# Add to crontab
crontab -e

# Add this line (runs every Sunday at 2 AM)
0 2 * * 0 /home/alfatih1309/project/api-pegadaian/cleanup_logs.sh 7
```

## API Endpoints for Monitoring

- `GET /health` - API health check
- `GET /cache-info` - Check data freshness
- `POST /scrape` - Manual scraping trigger
- `GET /gold-prices` - Latest scraped data

## Security Considerations

1. **Log file permissions:** Ensure logs are readable only by appropriate users
2. **Script permissions:** Keep execute permissions restricted
3. **API access:** Consider adding authentication for production
4. **Network security:** Use HTTPS for external API access

## Performance Optimization

1. **Timing:** Avoid peak hours for scraping
2. **Resources:** Monitor CPU/memory usage
3. **Caching:** Leverage API caching effectively
4. **Cleanup:** Regular log maintenance

## Maintenance Tasks

### Daily:
- Check automation status
- Review error logs

### Weekly:
- Clean old logs
- Check disk usage
- Review performance metrics

### Monthly:
- Update dependencies
- Review and optimize schedule
- Backup important data
