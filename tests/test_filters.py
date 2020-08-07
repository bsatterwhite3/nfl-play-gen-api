import pandas as pd


from playgen import filters


def test_play_type_filter():
    data = {'play_id': [1, 2, 3],
            'play_type': ['pass', 'run', 'pass']}
    test_df = pd.DataFrame(data, columns=['play_id', 'play_type'])

    play_type_filter = filters.PlayTypeFilter('run')
    filtered_plays = play_type_filter.apply(test_df)

    assert len(filtered_plays) == 1
    assert filtered_plays.iloc[0].equals(pd.Series({'play_id': 2, 'play_type': 'run'}))


def test_field_position_filter():
    data = {'position': ['behind20', 'between20s', 'redzone', 'goalline'],
            'yardline_100': [15, 65, 87, 99]}
    test_df = pd.DataFrame(data, columns=['position', 'yardline_100'])

    behind_20_filter = filters.FieldPositionFilter('behind20')
    plays_behind_20 = behind_20_filter.apply(test_df)
    assert len(plays_behind_20) == 1
    assert plays_behind_20.iloc[0].equals(pd.Series({'position': 'behind20', 'yardline_100': 15}))

    between_20s_filter = filters.FieldPositionFilter('between20s')
    plays_between_20s = between_20s_filter.apply(test_df)
    assert len(plays_between_20s) == 1
    assert plays_between_20s.iloc[0].equals(pd.Series({'position': 'between20s', 'yardline_100': 65}))

    redzone_filter = filters.FieldPositionFilter('redzone')
    plays_redzone = redzone_filter.apply(test_df)
    assert len(plays_redzone) == 2
    assert plays_redzone.iloc[0].equals(pd.Series({'position': 'redzone', 'yardline_100': 87}))
    assert plays_redzone.iloc[1].equals(pd.Series({'position': 'goalline', 'yardline_100': 99}))

    goalline_filter = filters.FieldPositionFilter('goalline')
    plays_goalline = goalline_filter.apply(test_df)
    assert len(plays_goalline) == 1
    assert plays_goalline.iloc[0].equals(pd.Series({'position': 'goalline', 'yardline_100': 99}))
