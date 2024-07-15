from dotenv import load_dotenv
import os

load_dotenv()

# Configuration settings for the crawler
API_BASE_URL = 'https://play.google.com/store/apps'
DETAILS_URL = 'https://play.google.com/store/apps/details?id='
LOG_PATH = 'logs/crawler.log'

# Main sitemap URLs
MAIN_SITEMAPS = [
    'https://play.google.com/store/apps/details?id=com.ubercab',
]

# MySQL database configuration
MYSQL_CONFIG = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'db': os.getenv('MYSQL_DATABASE')
}
