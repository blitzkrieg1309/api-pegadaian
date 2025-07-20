from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import sys

# Tambahkan path untuk import scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.pegadaian_scraper import PegadaianScraperSelenium

# Inisialisasi FastAPI
app = FastAPI(
    title="Pegadaian Scraper API",
    description="API untuk mengambil data dari website Pegadaian.co.id",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scraper instance
scraper = PegadaianScraperSelenium()

# Pydantic models untuk response
class GoldPrice(BaseModel):
    timestamp: str
    buy_price: Optional[str] = None
    sell_price: Optional[str] = None
    last_updated: Optional[str] = None

class GoldBarPrice(BaseModel):
    weight: str
    price: str
    timestamp: str

class CompanyStats(BaseModel):
    timestamp: str
    total_assets: Optional[str] = None
    total_credit: Optional[str] = None
    total_branches: Optional[str] = None
    total_customers: Optional[str] = None

class NewsItem(BaseModel):
    title: str
    url: str
    timestamp: str

class ScrapingResponse(BaseModel):
    scrape_timestamp: str
    gold_prices: GoldPrice
    gold_bar_prices: List[GoldBarPrice]
    company_stats: CompanyStats
    latest_news: List[NewsItem]

# Cache untuk menyimpan data terakhir
cached_data = None
cache_timestamp = None

def get_cached_data_path() -> str:
    """Mendapatkan path file cache terbaru"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        return None
    
    json_files = [f for f in os.listdir(data_dir) if f.startswith("pegadaian_data_") and f.endswith(".json")]
    if not json_files:
        return None
    
    # Ambil file terbaru
    latest_file = sorted(json_files)[-1]
    return os.path.join(data_dir, latest_file)

def load_cached_data() -> Optional[Dict]:
    """Memuat data dari cache"""
    cache_path = get_cached_data_path()
    if not cache_path or not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

@app.get("/", tags=["General"])
async def root():
    """Endpoint root dengan informasi API"""
    return {
        "message": "Pegadaian Scraper API",
        "version": "1.0.0",
        "description": "API untuk mengambil data dari website Pegadaian.co.id",
        "endpoints": {
            "/scrape": "Melakukan scraping data terbaru",
            "/gold-prices": "Mendapatkan harga emas tabungan",
            "/gold-bar-prices": "Mendapatkan harga emas batangan",
            "/company-stats": "Mendapatkan statistik perusahaan",
            "/news": "Mendapatkan berita terbaru",
            "/all-data": "Mendapatkan semua data"
        }
    }

@app.post("/scrape", response_model=ScrapingResponse, tags=["Scraping"])
async def scrape_data(background_tasks: BackgroundTasks):
    """Melakukan scraping data dari website Pegadaian"""
    try:
        # Jalankan scraping
        data = scraper.scrape_all_data()
        
        # Simpan ke file di background
        background_tasks.add_task(scraper.save_to_json, data)
        background_tasks.add_task(scraper.save_to_csv, data)
        
        # Update cache global
        global cached_data, cache_timestamp
        cached_data = data
        cache_timestamp = datetime.now()
        
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")

@app.get("/gold-prices", response_model=GoldPrice, tags=["Gold Prices"])
async def get_gold_prices():
    """Mendapatkan harga emas tabungan (beli/jual)"""
    try:
        # Coba ambil dari cache dulu
        data = load_cached_data()
        if not data:
            # Jika tidak ada cache, lakukan scraping
            data = scraper.scrape_all_data()
        
        return data.get('gold_prices', {})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching gold prices: {str(e)}")

@app.get("/gold-bar-prices", response_model=List[GoldBarPrice], tags=["Gold Prices"])
async def get_gold_bar_prices():
    """Mendapatkan harga emas batangan"""
    try:
        # Coba ambil dari cache dulu
        data = load_cached_data()
        if not data:
            # Jika tidak ada cache, lakukan scraping
            data = scraper.scrape_all_data()
        
        return data.get('gold_bar_prices', [])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching gold bar prices: {str(e)}")

@app.get("/company-stats", response_model=CompanyStats, tags=["Company"])
async def get_company_stats():
    """Mendapatkan statistik perusahaan"""
    try:
        # Coba ambil dari cache dulu
        data = load_cached_data()
        if not data:
            # Jika tidak ada cache, lakukan scraping
            data = scraper.scrape_all_data()
        
        return data.get('company_stats', {})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company stats: {str(e)}")

@app.get("/news", response_model=List[NewsItem], tags=["News"])
async def get_latest_news(limit: int = 5):
    """Mendapatkan berita terbaru"""
    try:
        # Coba ambil dari cache dulu
        data = load_cached_data()
        if not data:
            # Jika tidak ada cache, lakukan scraping
            data = scraper.scrape_all_data()
        
        news = data.get('latest_news', [])
        return news[:limit]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/all-data", response_model=ScrapingResponse, tags=["Data"])
async def get_all_data():
    """Mendapatkan semua data yang tersedia"""
    try:
        # Coba ambil dari cache dulu
        data = load_cached_data()
        if not data:
            # Jika tidak ada cache, lakukan scraping
            data = scraper.scrape_all_data()
        
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all data: {str(e)}")

@app.get("/cache-info", tags=["General"])
async def get_cache_info():
    """Mendapatkan informasi tentang cache data"""
    cache_path = get_cached_data_path()
    
    if cache_path and os.path.exists(cache_path):
        file_stat = os.stat(cache_path)
        return {
            "cache_available": True,
            "cache_file": cache_path,
            "cache_size_bytes": file_stat.st_size,
            "last_modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
    else:
        return {
            "cache_available": False,
            "message": "No cache data available"
        }

@app.delete("/cache", tags=["General"])
async def clear_cache():
    """Menghapus cache data"""
    try:
        data_dir = "data"
        if os.path.exists(data_dir):
            json_files = [f for f in os.listdir(data_dir) if f.startswith("pegadaian_data_") and f.endswith(".json")]
            deleted_files = []
            
            for file in json_files:
                file_path = os.path.join(data_dir, file)
                os.remove(file_path)
                deleted_files.append(file)
            
            # Clear global cache
            global cached_data, cache_timestamp
            cached_data = None
            cache_timestamp = None
            
            return {
                "message": "Cache cleared successfully",
                "deleted_files": deleted_files
            }
        else:
            return {"message": "No cache directory found"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")

# Health check endpoint
@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Pegadaian Scraper API"
    }
