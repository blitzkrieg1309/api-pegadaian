# Pegadaian Scraper API - Ubuntu Server Setup

Aplikasi web scraper untuk mengambil data dari website Pegadaian.co.id dan menyajikannya melalui REST API.

## 📋 Requirements

- Ubuntu Server 20.04 atau lebih baru
- Python 3.8+
- Google Chrome (untuk Selenium)
- ChromeDriver

## 🚀 Quick Setup

```bash
# 1. Clone atau upload project ke server
# 2. Masuk ke direktori project
cd /path/to/pegadaian-project

# 3. Jalankan script setup
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

## 🔧 Manual Setup

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dan pip
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f3 | cut -d '.' -f1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")
wget -N "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip
```

### 2. Setup Python Environment

```bash
# Buat virtual environment
python3 -m venv venv

# Aktivasi virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Jalankan API

```bash
# Development mode
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001

# Production mode dengan systemd (otomatis disetup oleh script)
sudo systemctl start pegadaian-api
```

## 📊 API Endpoints

- `GET /` - Informasi API
- `POST /scrape` - Scraping data baru dari website
- `GET /gold-prices` - Harga emas tabungan
- `GET /gold-bar-prices` - Harga emas batangan
- `GET /company-stats` - Statistik perusahaan
- `GET /news` - Berita terbaru
- `GET /all-data` - Semua data
- `GET /health` - Health check

## 🔧 Management Commands

```bash
# Start service
sudo systemctl start pegadaian-api

# Stop service
sudo systemctl stop pegadaian-api

# Restart service
sudo systemctl restart pegadaian-api

# Check status
sudo systemctl status pegadaian-api

# View logs
sudo journalctl -u pegadaian-api -f

# Enable auto-start on boot
sudo systemctl enable pegadaian-api
```

## 📁 Project Structure

```
pegadaian-project/
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── pegadaian_scraper.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── data/                    # Hasil scraping
├── venv/                    # Virtual environment
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── setup_ubuntu.sh         # Setup script
└── README.md
```

## 🐛 Troubleshooting

### Chrome/ChromeDriver Issues
```bash
# Check Chrome version
google-chrome --version

# Check ChromeDriver version
chromedriver --version

# Reinstall ChromeDriver jika versi tidak cocok
# (ikuti langkah install ChromeDriver di atas)
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/project

# Fix permissions
chmod +x setup_ubuntu.sh
chmod 755 venv/bin/activate
```

### Memory Issues (untuk VPS kecil)
```bash
# Jalankan Chrome dengan opsi headless dan limited memory
# (sudah dikonfigurasi di scraper)

# Monitor memory usage
htop
free -h
```

## 🔐 Security Notes

- API berjalan di port 8000 secara default
- Untuk production, pertimbangkan menggunakan reverse proxy (nginx)
- Setup firewall sesuai kebutuhan
- Monitor logs secara berkala

## 📝 Logs

```bash
# API logs
sudo journalctl -u pegadaian-api -f

# Chrome/Selenium logs ada di terminal output
# Data scraping tersimpan di folder data/
```
