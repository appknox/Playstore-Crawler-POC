import aiohttp
import asyncio
from bs4 import BeautifulSoup
from src.database import save_to_db_async
import logging

sem = asyncio.Semaphore(10)  # Limit to 10 concurrent requests

async def fetch(session, url):
    async with sem:
        async with session.get(url) as response:
            response.raise_for_status()
            
            # Check for encoding
            charset = 'ISO-8859-1'
            content = await response.read()
            return content.decode(charset)

async def fetch_metadata(app):
    async with aiohttp.ClientSession() as session:
        url = app['url']
        html = await fetch(session, url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')  # Use HTML parser
            # Extract app details
            try:
                title = soup.find('h1', class_='AHFaub').text if soup.find('h1', class_='AHFaub') else ''
                description_tag = soup.find('div', {'jsname': 'sngebd'})
                description = description_tag.text if description_tag else ''
                
                developer_name_tag = soup.find('a', class_='hrTbp R8zArc')
                developer_name = developer_name_tag.text if developer_name_tag else ''
                
                developer_email_tag = soup.find('a', href=lambda href: href and 'mailto:' in href)
                developer_email = developer_email_tag.get('href').replace('mailto:', '') if developer_email_tag else ''
                
                developer_website_tag = soup.find('a', class_='hrTbp euBY6b')
                developer_website = developer_website_tag.get('href') if developer_website_tag else ''
                
                icon_tag = soup.find('img', class_='T75of')
                icon = icon_tag.get('src') if icon_tag else ''
                
                screenshots_tags = soup.find_all('img', class_='T75of')
                screenshots = [img.get('src') for img in screenshots_tags] if screenshots_tags else []

                category = soup.find('a', itemprop='genre').text if soup.find('a', itemprop='genre') else ''
                rating = soup.find('div', class_='BHMmbe').text if soup.find('div', class_='BHMmbe') else ''
                number_of_reviews_tag = soup.find('span', {'class': 'EymY4b'})
                number_of_reviews = number_of_reviews_tag.find('span').text if number_of_reviews_tag else ''
                installs_tag = soup.find_all('div', class_='hAyfc')
                installs = installs_tag[2].find_all('span', {'class': 'htlgb'})[0].text if len(installs_tag) > 2 else ''

                data = {
                    'app_id': app['app_id'],
                    'package_name': app['app_id'],
                    'app_url': url,
                    'title': title,
                    'description': description,
                    'developer_name': developer_name,
                    'developer_website': developer_website,
                    'developer_email': developer_email,
                    'icon': icon,
                    'screenshots': screenshots,
                    'category': category,
                    'rating': rating,
                    'number_of_reviews': number_of_reviews,
                    'installs': installs
                }
                logging.info(f"Fetched metadata for app ID: {app['app_id']}")
                return data
            except Exception as e:
                logging.error(f"Error fetching metadata for app ID: {app['app_id']}, URL: {url}, Error: {e}")
                return None

async def fetch_metadata_in_parallel(apps):
    tasks = [fetch_metadata(app) for app in apps]
    results = await asyncio.gather(*tasks)
    results = [result for result in results if result is not None]
    logging.info(f"Fetched metadata for {len(results)} apps")
    return results

async def save_metadata_to_db(pool, metadata):
    if not metadata:
        logging.error("No metadata to save, skipping save to DB.")
        return
    async with pool.acquire() as conn:
        for data in metadata:
            await save_to_db_async(conn, data)
            logging.info(f"Fetched and saved metadata for app_id: {data['app_id']}")