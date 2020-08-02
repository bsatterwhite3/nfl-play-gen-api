

class PlaySampler(object):

    def __init__(self, play_by_play_data):
        self.play_by_play_data = play_by_play_data

    def sample_play(self, num_plays, with_replacement=False, filters=None):
        raise NotImplementedError

