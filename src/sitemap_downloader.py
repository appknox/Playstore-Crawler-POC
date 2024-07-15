import requests
from config.settings import MAIN_SITEMAPS
import logging
from src.utils import retry

@retry(requests.exceptions.RequestException, tries=3, delay=2, backoff=2)
def download_sitemap(url):
    try:
        response = requests.get(url, verify=True)  # Ensure SSL verification
        response.raise_for_status()
        
        # Check for encoding
        charset = 'ISO-8859-1'
        print(f"Encoding for {url}: {charset}")  # Logging statement to check encoding

        return response.content.decode(charset)
    except Exception as e:
        logging.error(f"Error downloading sitemap from {url}: {e}")
        return ''

def process_sitemap(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, features="html.parser")  # Use HTML parser
    app_urls = [a['href'] for a in soup.select('a[href^="/store/apps/details"]')]
    full_urls = ['https://play.google.com' + url for url in app_urls]
    return full_urls
