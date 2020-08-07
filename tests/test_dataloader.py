import os
import pandas as pd

from playgen import dataloader


def test_load_pbp_data_local(mocker):
    mocker.patch('playgen.dataloader.is_data_cached', return_value=True)
    mock_load = mocker.patch('playgen.dataloader.load_from_local')

    dataloader.load_pbp_data()
    mock_load.assert_called_once()


def test_load_pbp_data_repo(mocker):
    mocker.patch('playgen.dataloader.is_data_cached', return_value=False)
    mock_load = mocker.patch('playgen.dataloader.load_from_repo')
    mock_cache = mocker.patch('playgen.dataloader.cache_pbp_data')

    dataloader.load_pbp_data()
    mock_load.assert_called_once()
    mock_cache.assert_called_once()


def test_determine_path(mocker):
    mocker.patch('os.path.dirname', return_value='root')
    expected_path = 'root/../cache/data.csv.gz'
    result = dataloader.determine_cache_path()
    assert result == expected_path


def test_is_data_cached():
    dirname = os.path.dirname(__file__)
    cache_path = os.path.join(dirname, 'data/testdata.csv')

    assert dataloader.is_data_cached(cache_path)

    dirname = os.path.dirname(__file__)
    cache_path = os.path.join(dirname, 'data/fakedata.csv')

    assert not dataloader.is_data_cached(cache_path)


def test_load_from_local(mocker):
    cache_path = 'file.csv.gz'
    mock_local_load = mocker.patch('playgen.dataloader.pd.read_csv')
    dataloader.load_from_local(cache_path)

    mock_local_load.assert_called_with(cache_path, compression="gzip")


def test_load_from_repo(mocker):
    expected_calls = []
    years = [2019, 2018]
    for year in years:
        expected_calls.append(mocker.call(
            f"https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_{year}.csv.gz?raw=True",
            compression="gzip",
            low_memory=False
        ))

    mock_repo_load = mocker.patch('playgen.dataloader.pd.read_csv', return_value=pd.DataFrame())
    dataloader.load_from_repo()

    mock_repo_load.assert_has_calls(expected_calls)
