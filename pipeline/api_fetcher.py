import io
import json
import requests

from datetime import datetime, timezone
from ratelimit import limits, sleep_and_retry

from pipeline._utils import logger

OW_KEY = 'f2b5d36fc1f975ace88d6ac18f0d6f42'
PARAMETERS = {
    'start':'1',
    'limit':'200',
}
HEADERS = {
    'Accepts': 'application/json',
}


def construct_url_for_city(city_name: str, country_name: str, limit: int, key: str):
    return (f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_name}&'
            f'limit={limit}&appid={key}')



@sleep_and_retry
@limits(calls=2, period=30)  # max 2 call every 30 seconds
@sleep_and_retry
@limits(calls=500, period=3600)  # max 500 calls every hour
def call_listings_endpoint(city: str, country: str, limit:int, key:str, **kwargs):
    request = requests.Request('GET',
                               url=(url:=construct_url_for_city(city, country, limit,key)),
                               headers=kwargs['headers'],
                               params=kwargs['params'])
    logger.info('Fetching {}?{}'.format(request.url, request.params))
    response = requests.Session().send(request.prepare())
    if response.status_code != 200:
        raise Exception(f"Got HTTP response {response.status_code} when fetching URL: {url}. "
                        f"Response: {response.text}")
    return response

"""
Raw data keys:
>>> raw_data['data'][0].keys()
dict_keys(['id', 'name', 'title', 'description', 'num_tokens', 'avg_price_change', 'market_cap', \
    'market_cap_change', 'volume', 'volume_change', 'last_updated'])

"""

def extract_response_data(api_response: requests.Response):
    """
    Store the raw api call fetch to a local dir 'data/raw_data.json' (consider partitioning)
    """
    raw_content = json.loads(io.BytesIO(api_response.content).read().decode('utf-8'))


def store_raw_data(raw_data: dict, dest_file: str):
    with open(dest_file, 'w') as f:
            json.dump(raw_data, f)







def store_api_metrics(api_response: requests.Response):
    """
    (optional) Store api call metrics for further analysis. Store in a local csv file or
    something similar
    :return:
    """
    status_code = api_response.status_code
    metrics = (
        datetime.strptime(api_response.headers['Date'], '%a, %d %b %Y %H:%M:%S GMT').isoformat(),
        api_response.status_code,
        api_response.url,
        api_response.elapsed.seconds/1.0,
    )
