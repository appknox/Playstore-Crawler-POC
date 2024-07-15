import aiomysql
import json
import logging

async def create_tables_async(conn):
    async with conn.cursor() as cursor:
        with open('data/schema.sql') as f:
            schema = f.read()
        for statement in schema.split(';'):
            if statement.strip():
                await cursor.execute(statement)
        await conn.commit()
        logging.info("Database tables created")

async def save_to_db_async(conn, data):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
            INSERT INTO apps (app_id, package_name, app_url, title, description, developer_name, developer_website, developer_email, icon, screenshots, category, rating, number_of_reviews, installs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            AS new
            ON DUPLICATE KEY UPDATE 
                package_name = new.package_name,
                app_url = new.app_url,
                title = new.title,
                description = new.description,
                developer_name = new.developer_name,
                developer_website = new.developer_website,
                developer_email = new.developer_email,
                icon = new.icon,
                screenshots = new.screenshots,
                category = new.category,
                rating = new.rating,
                number_of_reviews = new.number_of_reviews,
                installs = new.installs
            ''', (
                data['app_id'], data['package_name'], data['app_url'], data['title'],
                data['description'], data['developer_name'], data['developer_website'],
                data['developer_email'], data['icon'], json.dumps(data['screenshots']),
                data['category'], data['rating'], data['number_of_reviews'], data['installs']
            ))
            await conn.commit()
            logging.info(f"Saved app data to database for app_id: {data['app_id']}")
    except Exception as e:
        logging.error(f"Error saving app data for app_id: {data['app_id']}: {e}")

async def save_sitemap_data_async(conn, url, app_id, alternates):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
            INSERT INTO sitemaps (url, app_id, alternate_links)
            VALUES (%s, %s, %s)
            AS new
            ON DUPLICATE KEY UPDATE 
                app_id = new.app_id,
                alternate_links = new.alternate_links
            ''', (url, app_id, json.dumps(alternates)))
            await conn.commit()
            logging.info(f"Saved sitemap data to database for url: {url}")
    except Exception as e:
        logging.error(f"Error saving sitemap data for url: {url}: {e}")
