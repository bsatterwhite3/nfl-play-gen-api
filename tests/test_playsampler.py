import pytest
import os

import pandas as pd

from playgen import playsampler
from playgen.exceptions import InsufficientDataException


# @pytest.fixture
# def full_pbp_df():
#     dirname = os.path.dirname(__file__)
#     filename = os.path.join(dirname, 'data/testdata.csv')
#     return pd.read_csv(filename)


@pytest.fixture
def small_pbp_df():
    data = [
        ["J.Doe pass short left", 2.0, 2.8, 'CLE_DEN', 2507.0, 0, 1, 0.0, 'pass', 0, 1.0, 70.0, 4]
    ]
    columns = ['desc', 'down', 'epa', 'game_id', 'game_seconds_remaining', 'goal_to_go', 'pass', 'penalty',
               'play_type', 'rush', 'success', 'yardline_100', 'ydstogo']
    df = pd.DataFrame(data, columns=columns)
    return df


def test_sample_too_many_plays_error(full_pbp_df):
    size = len(full_pbp_df)
    num_plays = size + 1

    sampler = playsampler.PlaySampler(full_pbp_df)
    with pytest.raises(InsufficientDataException):
        sampler.sample(num_plays, with_replacement=False)


def test_sample_5(full_pbp_df):
    sampler = playsampler.PlaySampler(full_pbp_df)
    plays = sampler.sample(5, with_replacement=False)
    assert len(plays) == 5


def test_sample_with_replacement(full_pbp_df):
    single_row_df = full_pbp_df[2:3]
    sampler = playsampler.PlaySampler(single_row_df)

    result = sampler.sample(2, with_replacement=True)

    assert result[0] == result[1]


def test_convert_play_df_to_list(small_pbp_df):
    expected = [playsampler.Play(desc="J.Doe pass short left", down=2.0, epa=2.8, game_id='CLE_DEN',
                                 game_seconds_remaining=2507.0, goal_to_go=0, passing=1, penalty=0.0, play_type='pass',
                                 rushing=0, success=1.0, yardline_100=70.0, ydstogo=4)]
    result = playsampler.PlaySampler._convert_play_df_to_list(small_pbp_df)
    assert result == expected
