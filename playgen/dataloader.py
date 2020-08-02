import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_data():
    # Enter desired years of data
    YEARS = [2019]

    data = pd.DataFrame()

    for i in YEARS:
        i_data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                             'play_by_play_' + str(i) + '.csv.gz?raw=True',
                             compression='gzip', low_memory=False)

        # sort=True eliminates a warning and alphabetically sorts columns
        data = data.append(i_data, sort=True)

    # Give each row a unique index
    data.reset_index(drop=True, inplace=True)
    return data