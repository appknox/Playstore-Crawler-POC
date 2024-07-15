import sys
import os
import asyncio
import logging
import aiomysql

# Add the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sitemap_downloader import download_sitemap, process_sitemap
from sitemap_processor import process_sub_sitemaps
from metadata_fetcher import fetch_metadata_in_parallel
from utils import setup_logging, split_chunks
from database import create_tables_async, save_sitemap_data_async, save_to_db_async
from config.settings import MAIN_SITEMAPS, MYSQL_CONFIG

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

async def main():
    setup_logging()
    logging.info('Crawler started')

    # Create database tables
    pool = await aiomysql.create_pool(**MYSQL_CONFIG)
    async with pool.acquire() as conn:
        await create_tables_async(conn)

    # Only process the first 50 apps for testing
    total_apps = 0
    max_apps = 500

    for main_sitemap_batch in batch(MAIN_SITEMAPS, 1):
        try:
            logging.info(f"Processing batch of main sitemap: {main_sitemap_batch[0]}")
            sub_sitemaps = []
            
            # Download and process the main sitemap
            sitemap_content = download_sitemap(main_sitemap_batch[0])
            if sitemap_content:
                sub_sitemaps.extend(process_sitemap(sitemap_content))

            logging.info(f"Downloaded and processed {len(sub_sitemaps)} sub sitemaps")

            for sub_sitemap_batch in batch(sub_sitemaps, 10):
                if total_apps >= max_apps:
                    break

                sem = asyncio.Semaphore(10)  # Create a new semaphore for each loop
                sub_sitemap_data = await process_sub_sitemaps(sub_sitemap_batch, sem)
                
                async with pool.acquire() as conn:
                    for loc, app_id, alternates in sub_sitemap_data:
                        await save_sitemap_data_async(conn, loc, app_id, alternates)
                        logging.info(f"Saved sitemap data for URL: {loc}")

                logging.info(f"Processed {len(sub_sitemap_batch)} sub sitemaps")

                apps_to_process = [{'url': loc, 'app_id': app_id} for loc, app_id, _ in sub_sitemap_data[:max_apps - total_apps]]
                metadata = await fetch_metadata_in_parallel(apps_to_process)
                async with pool.acquire() as conn:
                    for data in metadata:
                        await save_to_db_async(conn, data)
                        logging.info(f"Fetched and saved metadata for app_id: {data['app_id']}")
                        total_apps += 1

                if total_apps >= max_apps:
                    break

            if total_apps >= max_apps:
                break

            logging.info(f"Processed and saved batch of main sitemap")
        except Exception as e:
            logging.error(f"An error occurred while processing batch: {e}")

    pool.close()
    await pool.wait_closed()
    logging.info('Crawler finished')

if __name__ == '__main__':
    asyncio.run(main())