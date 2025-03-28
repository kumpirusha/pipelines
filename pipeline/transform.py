import numpy as np
import json

from pandas import DataFrame, to_datetime

from pipeline.utils import logger
from pipeline.constants import TABLE_COLUMN_MAP


def read_raw_data(raw_data_location: str) -> dict:
    """
    Pick up raw data files from local folder and load it into memory
    :return:
    """
    logger.info(f'Reading raw data from {raw_data_location}')
    with open(raw_data_location, 'rb') as rf:
        return json.load(rf)


def transform_data(flat_data: dict) -> DataFrame:
    logger.info(f'Transforming and cleaning flattened data...')
    df = DataFrame(flat_data, index=[0])
    # insert empty columns if missing
    for n, i in enumerate(TABLE_COLUMN_MAP):
        if i not in df.columns:
            df.insert(loc=n, column=i, value=np.nan)
    df = df[list(TABLE_COLUMN_MAP.keys())]  # Filter out unused cols
    df.rename(columns=TABLE_COLUMN_MAP, inplace=True)  # Rename columns

    for c in ['datetime', 'sunrise', 'sunset']:
        df[c] = to_datetime(df[c], utc=True, unit='s')
    logger.info('Data clean-up complete')

    return df


def write_transformed_data(clean_table: DataFrame, write_location: str):
    logger.info(f'Writing clean data to {write_location}')
    clean_table.to_json(write_location, orient='split', index=False)
