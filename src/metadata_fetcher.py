import aiohttp
import asyncio
from bs4 import BeautifulSoup
from database import save_to_db

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_metadata(app):
    async with aiohttp.ClientSession() as session:
        url = app['url']
        html = await fetch(session, url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Extract app details
            data = {
                'app_id': app['app_id'],
                'package_name': app['app_id'],
                'app_url': url,
                'title': soup.find('h1', class_='AHFaub').text if soup.find('h1', class_='AHFaub') else '',
                'description': soup.find('div', jsname='sngebd').text if soup.find('div', jsname='sngebd') else '',
                'developer_name': soup.find('a', class_='hrTbp R8zArc').text if soup.find('a', class_='hrTbp R8zArc') else '',
                'developer_website': soup.find('a', class_='hrTbp euBY6b').text if soup.find('a', class_='hrTbp euBY6b') else '',
                'developer_email': soup.find('a', class_='hrTbp').text if soup.find('a', class_='hrTbp') else '',
                'icon': soup.find('img', class_='T75of').get('src') if soup.find('img', class_='T75of') else '',
                'screenshots': [img.get('src') for img in soup.find_all('img', class_='T75of')] if soup.find_all('img', class_='T75of') else []
            }
            save_to_db(data)

async def fetch_metadata_in_parallel(apps):
    tasks = [fetch_metadata(app) for app in apps]
    await asyncio.gather(*tasks)
