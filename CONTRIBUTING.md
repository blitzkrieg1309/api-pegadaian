# Contributing to Pegadaian Scraper API

Terima kasih atas minat Anda untuk berkontribusi! 🎉

## 🔧 Development Setup

1. **Fork repository ini**
2. **Clone fork Anda:**
   ```bash
   git clone https://github.com/your-username/pegadaian-scraper-api.git
   cd pegadaian-scraper-api
   ```

3. **Setup environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   .\venv\Scripts\Activate.ps1  # Windows
   
   pip install -r requirements_clean.txt
   ```

## 📝 Pull Request Process

1. **Buat branch baru:**
   ```bash
   git checkout -b feature/nama-fitur
   ```

2. **Lakukan perubahan dan test:**
   ```bash
   # Test scraper
   python src/scraper/pegadaian_scraper.py
   
   # Test API
   python main.py
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: deskripsi perubahan"
   ```

4. **Push dan buat PR:**
   ```bash
   git push origin feature/nama-fitur
   ```

## 🎯 Contribution Guidelines

### Code Style
- Gunakan Python PEP 8 style guide
- Tambahkan docstring untuk functions/classes
- Gunakan type hints jika memungkinkan

### Commit Messages
Gunakan format conventional commits:
- `feat:` untuk fitur baru
- `fix:` untuk bug fixes
- `docs:` untuk dokumentasi
- `refactor:` untuk refactoring
- `test:` untuk testing

### Testing
- Test manual semua endpoint API
- Pastikan scraper bisa mengambil data
- Test di environment yang berbeda jika memungkinkan

## 🐛 Bug Reports

Jika menemukan bug:
1. Cek apakah sudah ada issue yang sama
2. Buat issue baru dengan template bug report
3. Sertakan:
   - OS dan Python version
   - Error message lengkap
   - Steps to reproduce
   - Expected vs actual behavior

## 💡 Feature Requests

Untuk request fitur baru:
1. Buat issue dengan template feature request
2. Jelaskan use case dan manfaatnya
3. Diskusikan implementasi jika perlu

## 📋 Areas for Contribution

- **Scraper improvements** - Menambah data yang bisa di-scrape
- **API enhancements** - Endpoint baru, filtering, pagination
- **Error handling** - Better error messages dan recovery
- **Performance** - Caching, rate limiting, optimization
- **Documentation** - Guides, tutorials, API docs
- **Testing** - Unit tests, integration tests
- **Deployment** - Docker, Kubernetes, cloud platforms

## ⚠️ Important Notes

- **Respect website terms of service** - Jangan scraping berlebihan
- **Rate limiting** - Implementasi delay yang wajar
- **Error handling** - Graceful degradation
- **Security** - Jangan commit credentials atau sensitive data

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

## 📞 Questions?

Jika ada pertanyaan:
- Buat issue dengan label `question`
- Diskusi di GitHub Discussions (jika tersedia)

Happy coding! 🚀
