# 🏪 Pegadaian Scraper API

Web scraper dan REST API untuk mengambil data dari website [Pegadaian.co.id](https://www.pegadaian.co.id/).

## ✨ Features

- 🥇 **Harga Emas Real-time** - Harga beli/jual emas tabungan terbaru
- 📊 **Statistik Perusahaan** - Total aset, kredit, cabang, dan nasabah
- 📰 **Berita Terbaru** - Update berita dari Pegadaian
- 🔄 **REST API** - Akses data melalui HTTP API
- 💾 **Data Caching** - Penyimpanan data lokal untuk performa
- 🐳 **Production Ready** - Setup otomatis untuk Ubuntu Server

## 🚀 Quick Start

### Development (Windows)

```bash
# 1. Clone project
git clone <repository-url>
cd pegadaian-project

# 2. Setup virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip install -r requirements_clean.txt

# 4. Run API
python main.py
```

### Production (Ubuntu Server)

```bash
# 1. Upload project ke server
# 2. Jalankan setup otomatis
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh

# 3. Start service
sudo systemctl start pegadaian-api
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Informasi API |
| `/health` | GET | Health check |
| `/scrape` | POST | Scraping data baru |
| `/gold-prices` | GET | Harga emas tabungan |
| `/gold-bar-prices` | GET | Harga emas batangan |
| `/company-stats` | GET | Statistik perusahaan |
| `/news` | GET | Berita terbaru |
| `/all-data` | GET | Semua data |

## 🔧 Configuration

Copy `.env.example` ke `.env` dan sesuaikan:

```env
API_HOST=0.0.0.0
API_PORT=8000
SCRAPER_HEADLESS=true
CACHE_ENABLED=true
```

## 📊 Usage Examples

### Mendapatkan Harga Emas

```bash
curl http://localhost:8001/gold-prices
```

```json
{
  "timestamp": "2025-07-20T14:03:00.908962",
  "buy_price": "18.470,00",
  "sell_price": "17.820,00",
  "last_updated": "20 Jul 2025 12:00:01"
}
```

### Scraping Data Baru

```bash
curl -X POST http://localhost:8001/scrape
```

### Mendapatkan Semua Data

```bash
curl http://localhost:8001/all-data
```

## 🏗️ Project Structure

```
pegadaian-project/
├── src/
│   ├── scraper/           # Web scraping logic
│   ├── api/              # FastAPI application
│   └── utils/            # Helper functions
├── data/                 # Scraped data storage
├── main.py              # Application entry point
├── requirements_clean.txt # Python dependencies
├── setup_ubuntu.sh      # Ubuntu setup script
├── UBUNTU_SETUP.md      # Ubuntu setup guide
└── PRODUCTION.md        # Production deployment guide
```

## 🛠️ Tech Stack

- **Python 3.8+** - Programming language
- **FastAPI** - Web framework untuk API
- **Selenium** - Web browser automation
- **BeautifulSoup** - HTML parsing
- **Requests** - HTTP client
- **Pandas** - Data manipulation
- **Chrome/ChromeDriver** - Web browser untuk scraping

## 📚 Documentation

- [Ubuntu Setup Guide](UBUNTU_SETUP.md) - Setup untuk Ubuntu Server
- [Production Deployment](PRODUCTION.md) - Production deployment guide

## 🔧 Development

### Setup Development Environment

```bash
# Install dependencies
pip install -r requirements_clean.txt

# Run tests
pytest tests/

# Run with auto-reload
uvicorn main:app --reload --port 8001
```

### Project Commands

```bash
# Manual scraping
python src/scraper/pegadaian_scraper.py

# Run API server
python main.py

# Ubuntu deployment
./deploy.sh server-ip username
```

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8001/health
```

### Logs

```bash
# Ubuntu systemd logs
sudo journalctl -u pegadaian-api -f

# Application logs
tail -f logs/api.log
```

## 🚨 Troubleshooting

### Common Issues

1. **ChromeDriver version mismatch**
   ```bash
   # Check versions
   google-chrome --version
   chromedriver --version
   ```

2. **Permission denied**
   ```bash
   chmod +x setup_ubuntu.sh run_api.sh
   ```

3. **Port already in use**
   ```bash
# Change port in .env or command line
python main.py --port 8002
```## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan edukasi dan research. Pastikan untuk:
- Menghormati robots.txt dari website
- Tidak melakukan scraping berlebihan
- Menggunakan dengan bijak dan sesuai terms of service

## 📞 Support

Jika ada pertanyaan atau issue:
1. Check troubleshooting guide
2. Review documentation
3. Create GitHub issue
