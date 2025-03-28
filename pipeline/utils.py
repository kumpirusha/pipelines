import os
import logging
import requests

from psycopg2 import connect
from requests.exceptions import HTTPError

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture all log levels

# Create file handler
file_handler = logging.FileHandler("data/logs/etl.log")
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def call_endpoint(url, **kwargs) -> requests.Response | None:
    params = kwargs['parameters']
    logger.info(f'Fetching {url} with params: {params}')
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPError(
            f"Got HTTP response {response.status_code} when fetching URL: {url}. " f"Response: {response.text}"
        )
    else:
        return response


def flatten_dict(raw_data: dict, parent_key: str = '', sep: str = '_'):
    """
    Recursively flattens a nested dictionary.

    :param raw_data: Dictionary to flatten.
    :param parent_key: String prefix for nested keys.
    :param sep: Separator for nested keys.
    :return: Flattened dictionary.
    """
    items = []

    for k, v in raw_data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k  # Create flattened key

        if isinstance(v, dict):  # If value is a dictionary, recurse
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):  # If value is a list, iterate with index
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:  # Base case: store key-value pair
            items.append((new_key, v))

    return dict(items)


def generate_table_insert(table: str, columns: list, values: list | tuple) -> tuple:
    placeholders = ', '.join(['%s'] * len(values))

    return f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})", values


def create_tables():
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Connect to PostgreSQL
    logger.info(f'Establishing connection to database {DATABASE_URL}')
    conn = connect(DATABASE_URL)
    cursor = conn.cursor()

    logger.debug('Executing statements')
    # Create tables
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS api_metrics (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    call_dt TIMESTAMP,
    status_code INTEGER,
    safe_url TEXT,
    elapsed DOUBLE PRECISION,
    content_length INTEGER    
    );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS weather_data_clean (
    id SERIAL PRIMARY KEY, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    location_longitude        DOUBLE PRECISION,
    location_latitude         DOUBLE PRECISION,
    weather                  TEXT,
    weather_description       TEXT,
    temperature              DOUBLE PRECISION,
    feels_like               DOUBLE PRECISION,
    minimum_temperature      DOUBLE PRECISION,
    maximum_temperature      DOUBLE PRECISION,
    pressure                 INTEGER,
    humidity                 INTEGER,
    sea_level_pressure       INTEGER,
    ground_level_pressure    INTEGER,
    visibility               INTEGER,
    wind_speed               DOUBLE PRECISION,
    wind_direction_degrees   INTEGER,
    rain_precipitation       DOUBLE PRECISION,
    snow_precipitation       DOUBLE PRECISION,
    cloudiness_pct           INTEGER,
    datetime                 TIMESTAMPTZ,
    country                  TEXT,
    sunrise                  TIMESTAMPTZ,
    sunset                   TIMESTAMPTZ,
    timezone                 INTEGER,
    city_id                  INTEGER,
    city_name                TEXT
    );"""
    )
    logger.debug('Commiting changes')
    conn.commit()

    # Close connection
    logger.debug('Closing connections')
    cursor.close()
    conn.close()


def insert_data_into_table(statements: list[str, tuple]):
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Connect to PostgreSQL
    logger.info(f'Establishing connection to database {DATABASE_URL}')
    conn = connect(DATABASE_URL)
    cursor = conn.cursor()
    logger.info(f'Will execute {len(statements)} insert statements')
    for s in statements:
        cursor.execute(*s)
    logger.debug('Commiting changes')
    conn.commit()
    logger.debug('Closing connections')
    cursor.close()
    conn.close()
    logger.info('Table operations complete')
