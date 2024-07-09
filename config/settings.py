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
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'host': 'localhost',
    'database': 'playstore_crawler'
}
