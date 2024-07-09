import mysql.connector
import json
from config.settings import MYSQL_CONFIG

conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

def create_tables():
    with open('data/schema.sql') as f:
        schema = f.read()
    for statement in schema.split(';'):
        if statement.strip():
            cursor.execute(statement)

def save_to_db(data):
    cursor.execute('''
    INSERT INTO apps (app_id, package_name, app_url, title, description, developer_name, developer_website, developer_email, icon, screenshots)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        package_name = VALUES(package_name),
        app_url = VALUES(app_url),
        title = VALUES(title),
        description = VALUES(description),
        developer_name = VALUES(developer_name),
        developer_website = VALUES(developer_website),
        developer_email = VALUES(developer_email),
        icon = VALUES(icon),
        screenshots = VALUES(screenshots)
    ''', (
        data['app_id'], data['package_name'], data['app_url'], data['title'],
        data['description'], data['developer_name'], data['developer_website'],
        data['developer_email'], data['icon'], json.dumps(data['screenshots'])
    ))
    conn.commit()
