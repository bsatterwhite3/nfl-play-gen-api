import sys
import os
import logging

import pandas as pd


logger = logging.getLogger('app.dataloader')


def load_pbp_data() -> pd.DataFrame:
    """Loads nflfastR play-by-play cache into a pandas DataFrame.

    Reference: https://github.com/guga31bb/nflfastR-data#load-data-using-python

    Returns:
        pd.DataFrame: the play-by-play cache loaded from nflfastR
    """
    cache_path = determine_cache_path()
    if is_data_cached(cache_path):
        pbp_data = load_from_local(cache_path)
    else:
        pbp_data = load_from_repo()
        cache_pbp_data(pbp_data, cache_path)
    return pbp_data


def determine_cache_path() -> str:
    filename = "../cache/data.csv.gz"
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)


def is_data_cached(cache_path: str) -> bool:
    return os.path.exists(cache_path)


def load_from_local(cache_path: str) -> pd.DataFrame:
    logger.info(f"Reading cached data from local file: {cache_path}")
    data = pd.read_csv(cache_path, compression="gzip")
    return data


def load_from_repo():
    """Loads nflfastR play-by-play cache into a pandas DataFrame.

    Reference: https://github.com/guga31bb/nflfastR-data#load-data-using-python

    Returns:
        pd.DataFrame: the play-by-play cache loaded from nflfastR
    """
    years = [2019, 2018]

    data = pd.DataFrame()
    logger.info(f"Loading nflfastR play by play cache for years={years} into dataframe...")
    for year in years:
        year_data = pd.read_csv(
            f"https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=True",
            compression='gzip',
            low_memory=False
        )
        data = data.append(year_data, sort=True)
    data.reset_index(drop=True, inplace=True)
    return data


def cache_pbp_data(pbp_data: pd.DataFrame, cache_path: str):
    pbp_data.to_csv(cache_path, compression="gzip")
