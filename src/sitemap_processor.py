import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_sub_sitemap(url):
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)
        soup = BeautifulSoup(content, 'xml')
        # Extract URLs, app IDs, and alternate links with href lang
        data = []
        for url_tag in soup.find_all('url'):
            loc = url_tag.find('loc').text
            app_id = extract_app_id(loc)
            alternates = [(link['hreflang'], link['href']) for link in url_tag.find_all('xhtml:link')]
            data.append((loc, app_id, alternates))
        return data

def extract_app_id(url):
    # Logic to extract app ID from URL
    return url.split('id=')[-1]

async def process_sub_sitemaps(urls):
    tasks = [process_sub_sitemap(url) for url in urls]
    results = await asyncio.gather(*tasks)
    # Flatten the list of lists
    return [item for sublist in results for item in sublist]

def group_by_region(data):
    # Implement grouping logic
    grouped_data = {}
    for item in data:
        for hreflang, href in item[2]:
            if hreflang not in grouped_data:
                grouped_data[hreflang] = []
            grouped_data[hreflang].append({
                'url': item[0],
                'app_id': item[1],
                'alternate_link': href
            })
    return grouped_data
