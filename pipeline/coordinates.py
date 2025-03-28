import json

from requests.exceptions import HTTPError

from pipeline.utils import call_endpoint, logger
from pipeline.constants import CITY_URL, CITIES_TO_MONITOR, COORD_PARAMETERS


def fetch_city_coordinates():
    """
    Fetch coordinates for selected cities (one time job)
    """
    for c in CITIES_TO_MONITOR:
        logger.info(f'Fetching coordinates for city {c}')
        COORD_PARAMETERS['q'] = c
        try:
            resp = call_endpoint(CITY_URL, parameters=COORD_PARAMETERS)
            content = resp.json()[0]
            logger.info(f'City {c} has coordinates:\nlat - {(lat:=content["lat"])}\n' f'lon - {(lon:=content["lon"])}')
            CITIES_TO_MONITOR[c] = (lat, lon)
        except HTTPError as e:
            logger.error(f'HTTPError encountered: {e}')
            exit(1)
        except Exception as e:
            logger.error(f'Unhandled exception encountered: {e}')
            exit(1)

    # dump to json
    with open('data/cities.json', 'w') as f:
        json.dump(CITIES_TO_MONITOR, f)


if __name__ == '__main__':
    import os, sys

    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import pipeline.constants
