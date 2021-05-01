

"""Tests for page-loader package."""


import pytest
import tempfile
import pathlib

from page_loader.scripts.page_loader import download


@pytest.mark.skip(reason='deativated')
def test_download_check_filepath():
    assert download('https://ru.hexlet.io/courses', '/var/tmp') == '/var/tmp/ru-hexlet-io-courses.html'


def test_download_check_content(requests_mock):
    requests_mock.get('http://test.com', text='data')
    with tempfile.TemporaryDirectory() as directory_name:
        the_dir = pathlib.Path(directory_name)
        with open(download('http://test.com', the_dir)) as f:
            assert f.read() == 'data'
