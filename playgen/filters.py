import logging
import pandas as pd

logger = logging.getLogger('app.filters')


class Filter(object):

    def apply(self, df: pd.DataFrame):
        raise NotImplementedError


class PlayTypeFilter(Filter):
    def __init__(self, play_type):
        self.play_type = play_type

    def apply(self, df: pd.DataFrame):
        logger.info(f"Applying play type filter to DF for play_type={self.play_type}")
        filtered_df = df[df['play_type'] == self.play_type]
        return filtered_df

    def __eq__(self, other):
        if isinstance(other, PlayTypeFilter):
            return self.play_type == other.play_type
        else:
            return NotImplemented


class FieldPositionFilter(Filter):
    def __init__(self, field_position):
        self.field_position = field_position

    def apply(self, df: pd.DataFrame):
        logger.info(f"Applying field position filter to DF for field_position={self.field_position}")

        field_ranges = {
            'behind20': [81, 100],
            'between20s': [20, 80],
            'redzone': [0, 19],
            'goalline': [0, 3]
        }
        positions = field_ranges[self.field_position]
        filtered_df = df[df['yardline_100'].between(positions[0], positions[1])]

        return filtered_df

    def __eq__(self, other):
        if isinstance(other, FieldPositionFilter):
            return self.field_position == other.field_position
        else:
            return NotImplemented
