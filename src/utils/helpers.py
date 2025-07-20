import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
import json

logger = logging.getLogger(__name__)

def clean_price_text(price_text: str) -> Optional[str]:
    """
    Membersihkan dan mengekstrak harga dari teks
    """
    if not price_text:
        return None
    
    # Hapus karakter yang tidak perlu
    price_text = price_text.strip()
    
    # Extract harga dalam format "Rp 18.470,00"
    price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
    if price_match:
        return price_match.group(1)
    
    return None

def clean_weight_text(weight_text: str) -> Optional[str]:
    """
    Membersihkan teks berat emas
    """
    if not weight_text:
        return None
    
    weight_text = weight_text.strip()
    
    # Standardisasi format berat
    weight_match = re.search(r'([\d,\.]+)\s*gram?', weight_text, re.IGNORECASE)
    if weight_match:
        return f"{weight_match.group(1)} gram"
    
    return weight_text

def extract_numbers_from_text(text: str) -> List[str]:
    """
    Mengekstrak semua angka dari teks
    """
    if not text:
        return []
    
    numbers = re.findall(r'[\d,.]+', text)
    return numbers

def validate_gold_price_data(data: Dict) -> bool:
    """
    Memvalidasi data harga emas
    """
    required_fields = ['buy_price', 'sell_price']
    
    for field in required_fields:
        if field not in data or not data[field]:
            logger.warning(f"Missing or empty field: {field}")
            return False
    
    return True

def validate_gold_bar_data(data: List[Dict]) -> bool:
    """
    Memvalidasi data harga emas batangan
    """
    if not data:
        logger.warning("No gold bar data found")
        return False
    
    required_fields = ['weight', 'price']
    
    for item in data:
        for field in required_fields:
            if field not in item or not item[field]:
                logger.warning(f"Invalid gold bar item: missing {field}")
                return False
    
    return True

def format_currency(amount: Union[str, int, float]) -> str:
    """
    Memformat angka menjadi format currency Indonesia
    """
    if isinstance(amount, str):
        # Hapus karakter non-numeric kecuali titik dan koma
        amount = re.sub(r'[^\d,.]', '', amount)
        # Konversi ke float
        try:
            amount = float(amount.replace(',', ''))
        except ValueError:
            return str(amount)
    
    # Format dengan pemisah ribuan
    return f"Rp {amount:,.2f}".replace(',', '.')

def extract_timestamp_from_text(text: str) -> Optional[str]:
    """
    Mengekstrak timestamp dari teks update
    """
    if not text:
        return None
    
    # Pattern untuk "Diperbarui 20 Jul 2025 12:00:01"
    timestamp_pattern = r'Diperbarui\s+(\d{1,2})\s+(\w{3})\s+(\d{4})\s+(\d{1,2}):(\d{2}):(\d{2})'
    match = re.search(timestamp_pattern, text)
    
    if match:
        day, month_str, year, hour, minute, second = match.groups()
        
        # Konversi nama bulan ke angka
        month_map = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        
        month = month_map.get(month_str, '01')
        
        # Format menjadi ISO 8601
        try:
            timestamp = f"{year}-{month}-{day.zfill(2)}T{hour.zfill(2)}:{minute}:{second}"
            return timestamp
        except Exception as e:
            logger.error(f"Error formatting timestamp: {e}")
    
    return None

def save_debug_html(html_content: str, filename: str = None):
    """
    Menyimpan HTML untuk debugging
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_{timestamp}.html"
    
    filepath = f"data/{filename}"
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Debug HTML saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving debug HTML: {e}")

def load_json_data(filepath: str) -> Optional[Dict]:
    """
    Memuat data dari file JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None

def compare_data_changes(old_data: Dict, new_data: Dict) -> Dict:
    """
    Membandingkan perubahan data antara scraping lama dan baru
    """
    changes = {
        'timestamp': datetime.now().isoformat(),
        'gold_price_changes': {},
        'new_gold_bars': [],
        'news_updates': []
    }
    
    # Bandingkan harga emas
    if 'gold_prices' in old_data and 'gold_prices' in new_data:
        old_gold = old_data['gold_prices']
        new_gold = new_data['gold_prices']
        
        if old_gold.get('buy_price') != new_gold.get('buy_price'):
            changes['gold_price_changes']['buy_price'] = {
                'old': old_gold.get('buy_price'),
                'new': new_gold.get('buy_price')
            }
        
        if old_gold.get('sell_price') != new_gold.get('sell_price'):
            changes['gold_price_changes']['sell_price'] = {
                'old': old_gold.get('sell_price'),
                'new': new_gold.get('sell_price')
            }
    
    # Bandingkan berita (cek judul baru)
    if 'latest_news' in old_data and 'latest_news' in new_data:
        old_titles = {news['title'] for news in old_data['latest_news']}
        new_news = new_data['latest_news']
        
        for news in new_news:
            if news['title'] not in old_titles:
                changes['news_updates'].append(news)
    
    return changes

def retry_request(func, max_retries: int = 3, delay: float = 1.0):
    """
    Retry decorator untuk request yang gagal
    """
    import time
    
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
    
    return wrapper

class DataValidator:
    """
    Class untuk validasi data hasil scraping
    """
    
    @staticmethod
    def validate_complete_data(data: Dict) -> Dict:
        """
        Validasi data lengkap hasil scraping
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validasi struktur dasar
        required_keys = ['scrape_timestamp', 'gold_prices', 'gold_bar_prices', 'company_stats', 'latest_news']
        
        for key in required_keys:
            if key not in data:
                validation_result['errors'].append(f"Missing required key: {key}")
                validation_result['is_valid'] = False
        
        # Validasi harga emas
        if 'gold_prices' in data:
            gold_prices = data['gold_prices']
            if not gold_prices.get('buy_price') and not gold_prices.get('sell_price'):
                validation_result['warnings'].append("No gold prices found")
        
        # Validasi harga emas batangan
        if 'gold_bar_prices' in data:
            if not data['gold_bar_prices']:
                validation_result['warnings'].append("No gold bar prices found")
        
        # Validasi berita
        if 'latest_news' in data:
            if not data['latest_news']:
                validation_result['warnings'].append("No news found")
        
        return validation_result
