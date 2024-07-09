CREATE DATABASE IF NOT EXISTS playstore_crawler;

USE playstore_crawler;

CREATE TABLE IF NOT EXISTS apps (
    app_id VARCHAR(255) PRIMARY KEY,
    package_name VARCHAR(255),
    app_url VARCHAR(255),
    title TEXT,
    description TEXT,
    developer_name VARCHAR(255),
    developer_website VARCHAR(255),
    developer_email VARCHAR(255),
    icon VARCHAR(255),
    screenshots JSON
);
