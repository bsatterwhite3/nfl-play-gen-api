import pytest

from playgen import handlers, filters
from playgen.exceptions import InvalidArgumentException


def test_get_plays(full_pbp_df):
    args = {'fieldPosition': 'between20s',
            'playType': 'run',
            'numPlays': 2,
            'withReplacement': False}
    response, status_code = handlers.get_plays(full_pbp_df, args)

    assert len(response) == 2
    assert all(play['play_type'] == 'run' for play in response)
    assert all(20 <= play['yardline_100'] <= 80 for play in response)
    assert status_code == 200


def test_get_plays_invalid_argument(full_pbp_df):
    args = {'fieldPosition': 'invalid',
            'playType': 'run',
            'numPlays': 2,
            'withReplacement': False}
    response, status_code = handlers.get_plays(full_pbp_df, args)
    assert status_code == 500


def test_get_plays_insufficient_data(full_pbp_df):
    args = {'fieldPosition': 'between20s',
            'playType': 'run',
            'numPlays': 10000000,
            'withReplacement': False}
    response, status_code = handlers.get_plays(full_pbp_df, args)
    assert status_code == 404


def test_validate_args():
    with pytest.raises(InvalidArgumentException):
        handlers.validate_args({'fieldPosition': 'invalid'})

    handlers.validate_args({'fieldPosition': 'behind20'})


def test_determine_filters_from_args():
    args = {'fieldPosition': 'redzone',
            'playType': 'run'}

    expected_filters = [filters.PlayTypeFilter('run'), filters.FieldPositionFilter('redzone')]

    result = handlers.determine_filters_from_query(args)
    assert result == expected_filters
