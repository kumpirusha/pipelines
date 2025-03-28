import json

from datetime import datetime
from pandas import DataFrame, to_datetime

from pipeline._utils import logger


def read_raw_data(raw_data_location: str) -> DataFrame:
    """
    Pick up raw data files from local folder and load it into memory
    :return:
    """
    with open(raw_data_location, 'r') as rf:
        raw_json = json.load(rf)

    return DataFrame(raw_json)


# FIXME
def transform_data(table: DataFrame) -> DataFrame:
    # Add creation date
    table['datetime'] = to_datetime(datetime.now(), format='ISO8601', utc=True)
    # Transform last_update
    table['last_update'] = to_datetime(table['last_updated'], format='ISO8601', utc=True)

    return table


def write_transformed_data(clean_table: DataFrame, write_location: str):
    clean_table.to_json(write_location)
