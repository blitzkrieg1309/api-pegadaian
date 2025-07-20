import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import pandas as pd
from typing import Dict, List, Optional
import logging
import time
import re
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PegadaianScraperSelenium:
    """
    Web scraper untuk mengambil data dari website Pegadaian menggunakan Selenium
    """
    
    def __init__(self, headless: bool = True):
        self.base_url = "https://www.pegadaian.co.id"
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            logger.info("Trying to use requests instead...")
            self.driver = None
    
    def get_page_content(self, url: str, wait_time: int = 10) -> Optional[BeautifulSoup]:
        """
        Mengambil konten halaman web dengan Selenium atau requests
        """
        if self.driver:
            try:
                self.driver.get(url)
                # Tunggu halaman load
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(3)  # Tunggu JavaScript load
                
                html = self.driver.page_source
                return BeautifulSoup(html, 'html.parser')
            except Exception as e:
                logger.error(f"Error with Selenium: {e}")
                return self._fallback_requests(url)
        else:
            return self._fallback_requests(url)
    
    def _fallback_requests(self, url: str) -> Optional[BeautifulSoup]:
        """Fallback menggunakan requests"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error with requests: {e}")
            return None
    
    def scrape_gold_prices(self) -> Dict:
        """
        Mengambil data harga emas dengan berbagai metode pencarian
        """
        logger.info("Scraping gold prices...")
        soup = self.get_page_content(self.base_url)
        
        if not soup:
            return {}
        
        gold_data = {
            'timestamp': datetime.now().isoformat(),
            'buy_price': None,
            'sell_price': None,
            'last_updated': None
        }
        
        try:
            import re
            
            # Metode 1: Cari berdasarkan class box-jual-beli (struktur yang Anda temukan)
            jual_beli_box = soup.find('div', class_='box-jual-beli')
            if jual_beli_box:
                logger.info("Found box-jual-beli element")
                
                # Cari harga beli
                beli_section = jual_beli_box.find('div', class_='box-jual-beli__left')
                if beli_section:
                    price_elem = beli_section.find('p')
                    if price_elem:
                        price_text = price_elem.get_text().replace('\xa0', ' ').replace('&nbsp;', ' ')
                        logger.info(f"Buy price text found: {price_text}")
                        price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                        if price_match:
                            gold_data['buy_price'] = price_match.group(1)
                            logger.info(f"Buy price extracted: {gold_data['buy_price']}")
                
                # Cari harga jual
                jual_section = jual_beli_box.find('div', class_='box-jual-beli__right')
                if jual_section:
                    price_elem = jual_section.find('p')
                    if price_elem:
                        price_text = price_elem.get_text().replace('\xa0', ' ').replace('&nbsp;', ' ')
                        logger.info(f"Sell price text found: {price_text}")
                        price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                        if price_match:
                            gold_data['sell_price'] = price_match.group(1)
                            logger.info(f"Sell price extracted: {gold_data['sell_price']}")
            
            # Metode 2: Jika metode 1 gagal, cari berdasarkan heading "Beli Emas" dan "Jual Emas"
            if not gold_data['buy_price'] or not gold_data['sell_price']:
                logger.info("Trying method 2: search by headings")
                
                # Cari semua h6 yang mengandung "Beli Emas"
                beli_headings = soup.find_all('h6', string=re.compile(r'Beli\s*Emas', re.IGNORECASE))
                for heading in beli_headings:
                    if not gold_data['buy_price']:
                        # Cari sibling p element
                        parent = heading.parent
                        price_elem = parent.find('p') if parent else None
                        if price_elem:
                            price_text = price_elem.get_text().replace('\xa0', ' ').replace('&nbsp;', ' ')
                            price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                            if price_match:
                                gold_data['buy_price'] = price_match.group(1)
                                logger.info(f"Buy price found via heading: {gold_data['buy_price']}")
                                break
                
                # Cari semua h6 yang mengandung "Jual Emas"
                jual_headings = soup.find_all('h6', string=re.compile(r'Jual\s*Emas', re.IGNORECASE))
                for heading in jual_headings:
                    if not gold_data['sell_price']:
                        parent = heading.parent
                        price_elem = parent.find('p') if parent else None
                        if price_elem:
                            price_text = price_elem.get_text().replace('\xa0', ' ').replace('&nbsp;', ' ')
                            price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                            if price_match:
                                gold_data['sell_price'] = price_match.group(1)
                                logger.info(f"Sell price found via heading: {gold_data['sell_price']}")
                                break
            
            # Metode 3: Cari semua elemen p yang mengandung "Rp" dengan format lengkap
            if not gold_data['buy_price'] or not gold_data['sell_price']:
                logger.info("Trying method 3: search all price elements")
                
                # Cari semua elemen yang mengandung pola harga emas
                price_pattern = r'Rp\s*[\d,.]+.*?0,01\s*gr'
                all_elements = soup.find_all(string=re.compile(price_pattern, re.IGNORECASE))
                
                prices_found = []
                for elem in all_elements:
                    price_match = re.search(r'Rp\s*([\d,.]+)', str(elem))
                    if price_match:
                        prices_found.append(price_match.group(1))
                        logger.info(f"Found price: {price_match.group(1)}")
                
                # Jika ada 2 harga, anggap yang pertama beli, kedua jual
                if len(prices_found) >= 2:
                    if not gold_data['buy_price']:
                        gold_data['buy_price'] = prices_found[0]
                    if not gold_data['sell_price']:
                        gold_data['sell_price'] = prices_found[1]
                elif len(prices_found) == 1:
                    if not gold_data['buy_price']:
                        gold_data['buy_price'] = prices_found[0]
            
            # Metode 4: Cari menggunakan Selenium WebDriver secara langsung
            if self.driver and (not gold_data['buy_price'] or not gold_data['sell_price']):
                logger.info("Trying method 4: direct Selenium search")
                try:
                    # Cari elemen dengan class box-jual-beli
                    jual_beli_elements = self.driver.find_elements(By.CLASS_NAME, "box-jual-beli")
                    if jual_beli_elements:
                        jual_beli_elem = jual_beli_elements[0]
                        
                        # Cari harga beli
                        try:
                            beli_left = jual_beli_elem.find_element(By.CLASS_NAME, "box-jual-beli__left")
                            beli_price = beli_left.find_element(By.TAG_NAME, "p")
                            price_text = beli_price.text.replace('\xa0', ' ')
                            price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                            if price_match and not gold_data['buy_price']:
                                gold_data['buy_price'] = price_match.group(1)
                                logger.info(f"Selenium buy price: {gold_data['buy_price']}")
                        except Exception as e:
                            logger.warning(f"Selenium buy price search failed: {e}")
                        
                        # Cari harga jual
                        try:
                            jual_right = jual_beli_elem.find_element(By.CLASS_NAME, "box-jual-beli__right")
                            jual_price = jual_right.find_element(By.TAG_NAME, "p")
                            price_text = jual_price.text.replace('\xa0', ' ')
                            price_match = re.search(r'Rp\s*([\d,.]+)', price_text)
                            if price_match and not gold_data['sell_price']:
                                gold_data['sell_price'] = price_match.group(1)
                                logger.info(f"Selenium sell price: {gold_data['sell_price']}")
                        except Exception as e:
                            logger.warning(f"Selenium sell price search failed: {e}")
                
                except Exception as e:
                    logger.warning(f"Selenium direct search failed: {e}")
            
            # Cari timestamp update
            update_patterns = [
                r'Diperbarui\s+\d+\s+\w+\s+\d+\s+\d+:\d+:\d+',
                r'Update.*\d+\s+\w+\s+\d+',
                r'Terakhir.*diperbarui'
            ]
            
            for pattern in update_patterns:
                update_elem = soup.find(string=re.compile(pattern, re.IGNORECASE))
                if update_elem:
                    gold_data['last_updated'] = update_elem.strip()
                    break
        
        except Exception as e:
            logger.error(f"Error scraping gold prices: {e}")
        
        logger.info(f"Final gold data: {gold_data}")
        return gold_data
    
    def _find_price_near_element(self, element) -> Optional[str]:
        """
        Mencari harga di sekitar elemen tertentu
        """
        # Cari di siblings
        for sibling in element.find_next_siblings():
            price_match = re.search(r'Rp\s*([\d,]+)', sibling.get_text())
            if price_match:
                return price_match.group(1)
        
        # Cari di parent dan siblings
        if element.parent:
            parent_text = element.parent.get_text()
            price_match = re.search(r'Rp\s*([\d,]+)', parent_text)
            if price_match:
                return price_match.group(1)
        
        return None
    
    def scrape_company_stats(self) -> Dict:
        """
        Mengambil statistik perusahaan
        """
        logger.info("Scraping company statistics...")
        soup = self.get_page_content(self.base_url)
        
        if not soup:
            return {}
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'total_assets': None,
            'total_credit': None,
            'total_branches': None,
            'total_customers': None
        }
        
        try:
            # Cari angka besar (kemungkinan statistik)
            numbers = soup.find_all(string=re.compile(r'[\d,.]+\s*[TM]'))
            
            for num_text in numbers:
                text = num_text.strip()
                if 'T' in text:  # Triliun
                    if '102' in text or '103' in text:
                        stats['total_assets'] = text
                    elif '85' in text or '86' in text:
                        stats['total_credit'] = text
                elif 'juta' in text.lower() or 'Juta' in text:
                    stats['total_customers'] = text
            
            # Cari jumlah cabang
            branch_numbers = soup.find_all(string=re.compile(r'^\d{4}$'))
            for num in branch_numbers:
                if num.strip().isdigit() and len(num.strip()) == 4:
                    stats['total_branches'] = num.strip()
                    break
        
        except Exception as e:
            logger.error(f"Error scraping company stats: {e}")
        
        return stats
    
    def scrape_latest_news(self, limit: int = 5) -> List[Dict]:
        """
        Mengambil berita terbaru
        """
        logger.info("Scraping latest news...")
        soup = self.get_page_content(self.base_url)
        
        if not soup:
            return []
        
        news_list = []
        
        try:
            # Cari link yang kemungkinan berita
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link.get('href')
                title = link.get_text().strip()
                
                # Filter link yang kemungkinan berita
                if (href and title and 
                    len(title) > 20 and  # Judul cukup panjang
                    ('berita' in href.lower() or 
                     'news' in href.lower() or
                     'pegadaian' in title.lower())):
                    
                    # Pastikan URL lengkap
                    if href.startswith('/'):
                        href = self.base_url + href
                    elif not href.startswith('http'):
                        continue
                    
                    news_list.append({
                        'title': title,
                        'url': href,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    if len(news_list) >= limit:
                        break
        
        except Exception as e:
            logger.error(f"Error scraping news: {e}")
        
        return news_list
    
    def scrape_all_data(self) -> Dict:
        """
        Mengambil semua data dalam satu fungsi
        """
        logger.info("Starting comprehensive scraping with Selenium...")
        
        all_data = {
            'scrape_timestamp': datetime.now().isoformat(),
            'gold_prices': self.scrape_gold_prices(),
            'gold_bar_prices': [],  # Will be implemented separately
            'company_stats': self.scrape_company_stats(),
            'latest_news': self.scrape_latest_news()
        }
        
        logger.info("Scraping completed successfully")
        return all_data
    
    def save_to_json(self, data: Dict, filename: str = None) -> str:
        """
        Menyimpan data ke file JSON
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pegadaian_data_{timestamp}.json"
        
        filepath = f"data/{filename}"
        
        try:
            # Buat direktori data jika belum ada
            os.makedirs("data", exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return ""
    
    def save_to_csv(self, data: Dict, filename: str = None) -> str:
        """
        Menyimpan data ke file CSV
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pegadaian_data_{timestamp}.csv"
        
        filepath = f"data/{filename}"
        
        try:
            # Buat direktori data jika belum ada
            os.makedirs("data", exist_ok=True)
            
            # Siapkan data untuk CSV
            csv_data = []
            
            # Gold prices
            if 'gold_prices' in data and data['gold_prices']:
                gold_data = data['gold_prices']
                csv_data.append({
                    'type': 'gold_price',
                    'timestamp': data.get('scrape_timestamp', ''),
                    'item': 'gold_buy',
                    'value': gold_data.get('buy_price', ''),
                    'last_updated': gold_data.get('last_updated', '')
                })
                csv_data.append({
                    'type': 'gold_price',
                    'timestamp': data.get('scrape_timestamp', ''),
                    'item': 'gold_sell',
                    'value': gold_data.get('sell_price', ''),
                    'last_updated': gold_data.get('last_updated', '')
                })
            
            # Company stats
            if 'company_stats' in data and data['company_stats']:
                stats = data['company_stats']
                for key, value in stats.items():
                    if key != 'timestamp':
                        csv_data.append({
                            'type': 'company_stat',
                            'timestamp': data.get('scrape_timestamp', ''),
                            'item': key,
                            'value': str(value),
                            'last_updated': stats.get('timestamp', '')
                        })
            
            # News
            if 'latest_news' in data and data['latest_news']:
                for i, news in enumerate(data['latest_news']):
                    csv_data.append({
                        'type': 'news',
                        'timestamp': data.get('scrape_timestamp', ''),
                        'item': f'news_{i+1}',
                        'value': news.get('title', ''),
                        'last_updated': news.get('date', '')
                    })
            
            # Simpan ke CSV
            if csv_data:
                df = pd.DataFrame(csv_data)
                df.to_csv(filepath, index=False, encoding='utf-8')
                logger.info(f"Data saved to {filepath}")
                return filepath
            else:
                logger.warning("No data to save to CSV")
                return ""
                
        except Exception as e:
            logger.error(f"Error saving CSV data: {e}")
            return ""
    
    def close(self):
        """Tutup WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")

# Contoh penggunaan
if __name__ == "__main__":
    scraper = PegadaianScraperSelenium(headless=True)
    
    try:
        # Scrape semua data
        data = scraper.scrape_all_data()
        
        # Simpan ke JSON
        scraper.save_to_json(data)
        
        # Print hasil
        print("=== HASIL SCRAPING PEGADAIAN (SELENIUM) ===")
        print(f"Timestamp: {data['scrape_timestamp']}")
        print(f"Harga Emas: {data['gold_prices']}")
        print(f"Statistik Perusahaan: {data['company_stats']}")
        print(f"Jumlah Berita: {len(data['latest_news'])}")
        
        if data['latest_news']:
            print("\nBerita Terbaru:")
            for i, news in enumerate(data['latest_news'][:3]):
                print(f"{i+1}. {news['title']}")
    
    finally:
        scraper.close()
