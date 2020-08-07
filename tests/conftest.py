import pytest
import os


import pandas as pd


@pytest.fixture
def full_pbp_df():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data/testdata.csv')
    return pd.read_csv(filename)