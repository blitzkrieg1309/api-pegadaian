# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-20

### Added
- Initial release of Pegadaian Scraper API
- Web scraper untuk mengambil data dari Pegadaian.co.id
- REST API dengan FastAPI framework
- Selenium WebDriver support untuk dynamic content scraping
- Endpoints untuk:
  - `/gold-prices` - Harga emas tabungan (beli/jual)
  - `/company-stats` - Statistik perusahaan
  - `/news` - Berita terbaru
  - `/scrape` - Trigger scraping baru
  - `/all-data` - Semua data sekaligus
- Ubuntu Server deployment scripts
- Automatic setup dengan `setup_ubuntu.sh`
- Systemd service configuration
- Production deployment guide
- Docker-ready configuration
- Comprehensive documentation
- Error handling dan logging
- Data caching system
- Rate limiting considerations

### Features
- **Multi-method scraping** - Requests + Selenium fallback
- **Headless browser** - Optimized untuk server environment
- **Auto-retry mechanism** - Robust error handling
- **JSON/CSV export** - Multiple output formats
- **Health check endpoint** - Monitoring support
- **Environment configuration** - Easy customization
- **Production scripts** - Ready untuk deployment

### Technical Stack
- Python 3.8+
- FastAPI untuk REST API
- Selenium untuk web automation
- BeautifulSoup untuk HTML parsing
- Requests untuk HTTP client
- Pandas untuk data processing
- ChromeDriver untuk browser automation

### Documentation
- README.md dengan quick start guide
- UBUNTU_SETUP.md untuk server setup
- PRODUCTION.md untuk production deployment
- API documentation dengan OpenAPI/Swagger
- Troubleshooting guides

## [Unreleased]

### Planned Features
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Redis caching
- [ ] Database storage
- [ ] Authentication system
- [ ] Rate limiting middleware
- [ ] Webhook notifications
- [ ] Scheduled scraping
- [ ] Data analytics dashboard
- [ ] Mobile app support
