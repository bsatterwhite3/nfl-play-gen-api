import logging
import pandas as pd
import numpy as np

from typing import List
from playgen.filters import Filter
from playgen.exceptions import InsufficientDataException
logger = logging.getLogger('app.playsampler')


class Play(object):
    """DTO used to store relevant attributes of a play."""
    def __init__(
            self,
            game_id: str,
            play_type: str,
            down: float,
            yardline_100: float,
            game_seconds_remaining: float,
            passing: int,
            rushing: int,
            penalty: float,
            goal_to_go: int,
            ydstogo: int,
            desc: str,
            success: float,
            epa: float
    ):
        self.game_id = game_id
        self.play_type = play_type
        self.down = down
        self.yardline_100 = yardline_100
        self.game_seconds_remaining = game_seconds_remaining
        self.passing = passing
        self.rushing = rushing
        self.penalty = penalty
        self.goal_to_go = goal_to_go
        self.ydstogo = ydstogo
        self.desc = desc
        self.success = success
        self.epa = epa

    def serialize(self):
        return self.__dict__

    def __eq__(self, other):
        if isinstance(other, Play):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __repr__(self):
        return str(self.__dict__)


class PlaySampler(object):

    def __init__(self, pbp_data):
        self.pbp_data = pbp_data

    def sample(self, num_plays, with_replacement=False, filters=None) -> List[Play]:
        filtered_plays = self._apply_filters(self.pbp_data, filters) \
             if filters else self.pbp_data
        if not with_replacement and num_plays > len(filtered_plays):
            raise InsufficientDataException(f"Dataframe too small to sample {num_plays} plays without replacement")
        play_df: pd.DataFrame = filtered_plays.sample(n=num_plays, replace=with_replacement)
        plays = self._convert_play_df_to_list(play_df)
        return plays

    @staticmethod
    def _apply_filters(pbp_data: pd.DataFrame, filters: List[Filter]) -> pd.DataFrame:
        filtered_data = pbp_data
        for play_filter in filters:
            filtered_data = play_filter.apply(filtered_data)
        if len(filtered_data) == 0:
            raise InsufficientDataException("No data available that satisfies provided filters")
        return filtered_data

    @staticmethod
    def _convert_play_df_to_list(plays_df: pd.DataFrame):
        plays = []
        for _, row in plays_df.iterrows():
            play = Play(
                game_id=row.game_id,
                play_type=row.play_type,
                down=row.down,
                yardline_100=row.yardline_100,
                game_seconds_remaining=row.game_seconds_remaining,
                passing=int(row['pass']),  # pass is a reserved keyword in python
                rushing=int(row.rush),
                penalty=row.penalty,
                goal_to_go=int(row.goal_to_go),
                ydstogo=row.ydstogo,
                desc=row.desc,
                success=row.success,
                epa=row.epa
            )
            plays.append(play)
        return plays
