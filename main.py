import schedule
import time

from datetime import datetime
from pandas import concat

from pipeline.constants import API_METRICS_COLUMNS, WEATHER_PARAMETERS, WEATHER_URL
from pipeline.coordinates import fetch_city_coordinates
from pipeline.utils import flatten_dict, logger, generate_table_insert, create_tables, \
    insert_data_into_table
from pipeline.fetch import fetch_weather_data, load_city_coordinates, \
    store_raw_weather_data_locally, store_api_metrics
from pipeline.transform import transform_data, write_transformed_data


def main():
    logger.info(f'Starting weather data pipeline')
    # check for coordinates file
    logger.info(f'Generating city coordinates...')
    fetch_city_coordinates()
    logger.info(f'cities.json file successfully generated')

    # getting weather data
    city_coords = load_city_coordinates('data/cities.json')
    metrics = []
    raw_dicts = []
    clean_tables = []
    for city, coord in city_coords.items():
        logger.debug(f'Starting raw data fetch')
        raw_weather = fetch_weather_data(WEATHER_URL, *coord, city, WEATHER_PARAMETERS)
        raw_dicts.append(raw_weather.json())
        metrics.append(store_api_metrics(raw_weather))
        logger.debug(f'Finished fetching raw data')

        # Data transformation
        logger.debug('Starting raw weather data processing')
        flat_data = flatten_dict(raw_weather.json())
        clean_tables.append(transform_data(flat_data))
        logger.debug('Finished raw data processing')

    dt = datetime.utcnow().isoformat()
    # Write raw data to file
    store_raw_weather_data_locally(raw_dicts, f'data/raw_data/raw_weather_data_{dt}')
    final_table = concat(clean_tables)
    final_table.reset_index(drop=True, inplace=True)
    write_transformed_data(final_table, f'data/processed_data/processed_weather_data_{dt}')

    logger.debug('Connection to database')
    create_tables()
    queries = [generate_table_insert('api_metrics', API_METRICS_COLUMNS, m) for m in metrics]
    queries.extend(
        [generate_table_insert('weather_data_clean', list(final_table.columns), t) for t in
         list(final_table.itertuples(index=False, name=None))])
    insert_data_into_table(queries)
    logger.debug('Database operations complete')


if __name__ == '__main__':
    schedule.every(30).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
