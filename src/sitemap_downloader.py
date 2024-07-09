import requests
from config.settings import MAIN_SITEMAPS

def download_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_sub_sitemaps():
    sub_sitemaps = []
    for url in MAIN_SITEMAPS:
        sitemap_content = download_sitemap(url)
        sub_sitemaps.extend(process_sitemap(sitemap_content))
    return sub_sitemaps

def process_sitemap(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'xml')
    return [loc.text for loc in soup.find_all('loc')]
