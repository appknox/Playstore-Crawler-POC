import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from sitemap_downloader import get_sub_sitemaps
from sitemap_processor import group_by_region, process_sub_sitemaps
from metadata_fetcher import fetch_metadata_in_parallel
from utils import setup_logging, split_chunks
from database import create_tables
import logging

if __name__ == '__main__':
    setup_logging()
    logging.info('Crawler started')

    create_tables()

    # Fetch and process sub-sitemaps
    try:
        sub_sitemaps = get_sub_sitemaps()
        sub_sitemap_data = asyncio.run(process_sub_sitemaps(sub_sitemaps))
        
        # Group by regions and split into chunks
        grouped_data = group_by_region(sub_sitemap_data)  # Implement grouping logic
        chunks = list(split_chunks(grouped_data, 100))  # Adjust chunk size as needed

        # Fetch metadata in parallel
        for chunk in chunks:
            asyncio.run(fetch_metadata_in_parallel(chunk))
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info('Crawler finished')
