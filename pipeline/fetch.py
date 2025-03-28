import json
import requests

from datetime import datetime
from requests.exceptions import HTTPError

from pipeline.utils import call_endpoint, logger


def load_city_coordinates(coord_path: str) -> dict:
    logger.info(f'Loading city coordinates data')
    with open(coord_path, 'r') as co:
        return json.load(co)


def fetch_weather_data(url: str, lat: float, lon: float, city: str, params: dict) -> requests.Response:
    """
    Store the raw api call fetch to a local dir 'data/raw_data.json' (consider partitioning)
    """
    logger.info(f'Fetching current weather data for {city} ({lat}/{lon})')
    params['lat'] = lat
    params['lon'] = lon
    try:
        response = call_endpoint(url, parameters=params)
        logger.info('Successfully fetched weather data')
        return response
    except HTTPError as e:
        logger.error(f'HTTPError encountered: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'Unhandled exception encountered: {e}')
        exit(1)


def store_raw_weather_data_locally(raw_data: list[dict], dest_file: str):
    logger.info(f'Writing raw weather data to {dest_file}')
    with open(dest_file, 'w') as f:
        for raw in raw_data:
            json.dump(raw, f)
            f.write('\n')


def store_api_metrics(api_response: requests.Response) -> tuple:
    """
    (optional) Store api call metrics for further analysis. Store in a local csv file or
    something similar
    :return:
    """
    safe_url = '{}?{}'.format(api_response.url.split('?')[0], api_response.headers["X-cache-key"].split("?")[-1])
    dt = datetime.strptime(api_response.headers['Date'], '%a, %d %b %Y %H:%M:%S GMT').isoformat()
    logger.info(f'Collecting metrics for api call {safe_url} @ {dt}')
    return (
        dt,
        api_response.status_code,
        safe_url,
        api_response.elapsed.seconds / 1.0,
        api_response.headers['Content-Length'],
    )
