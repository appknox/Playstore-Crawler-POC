from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration settings for the crawler
API_BASE_URL = 'https://play.google.com/store/apps'
DETAILS_URL = 'https://play.google.com/store/apps/details?id='
LOG_PATH = 'logs/crawler.log'

# Main sitemap URLs
MAIN_SITEMAPS = [
    'https://play.google.com/sitemaps/sitemaps-index-0.xml',
    'https://play.google.com/sitemaps/sitemaps-index-1.xml'
]

# MySQL database configuration
MYSQL_CONFIG = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE')
}
