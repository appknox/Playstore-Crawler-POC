import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging

sem = asyncio.Semaphore(10)  # Limit to 10 concurrent requests

async def fetch(session, url, sem):
    async with sem:
        async with session.get(url) as response:
            response.raise_for_status()
            
            # Check for encoding
            charset = 'ISO-8859-1'
            print(f"Encoding for {url}: {charset}")  # Logging statement to check encoding
            
            content = await response.read()
            return content.decode(charset)

async def process_sub_sitemap(url, sem):
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url, sem)
        soup = BeautifulSoup(content, features="html.parser")  # Specify HTML parser
        data = []
        loc = url
        app_id = extract_app_id(loc)
        alternates = [(link['hreflang'], link['href']) for link in soup.find_all('link', rel='alternate')]
        data.append((loc, app_id, alternates))
        return data

def extract_app_id(url):
    return url.split('id=')[-1]

async def process_sub_sitemaps(urls, sem):
    tasks = [process_sub_sitemap(url, sem) for url in urls]
    results = await asyncio.gather(*tasks)
    return [item for sublist in results for item in sublist]