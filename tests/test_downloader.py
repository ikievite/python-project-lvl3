

"""Test downloader module."""


import os
import pathlib
import tempfile
import logging
import pytest

import bs4

import requests_mock
from page_loader.downloader import (HTML_EXTENSION, download, write_file,
                                    format_url)
from page_loader.helpers import get_content


logger = logging.getLogger(__name__)

test_urls = [
    ('https://ru.hexlet.io/courses', HTML_EXTENSION, 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png', '', 'ru-hexlet-io-assets-professions-nodejs.png'),
]


@pytest.mark.parametrize("url, extention, expected", test_urls)
def test_format_url(url, extention, expected):
    logger.debug('Testing format_url function')
    result = format_url(url, extention)
    assert result == expected


def test_write_file(sample_file='tests/fixtures/original.original'):
    with open(sample_file, 'rb') as f:
        sample_file = f.read()
    dl_path = 'http://test.com/thefile.file'

    with requests_mock.Mocker() as mock:
        # Return any size (doesn't matter, only for prints)
        mock.head(requests_mock.ANY, headers={'Content-Length': '100'})

        mock.get(dl_path, content=sample_file)

        with tempfile.TemporaryDirectory() as directory_name:
            the_dir = pathlib.Path(directory_name)
            target_path = os.path.join(the_dir, 'test.file')
            write_file(dl_path, target_path)

            assert os.path.isfile(target_path)

            with open(target_path, 'rb') as f:
                assert f.read() == sample_file


def test_download_check_content(requests_mock):
    requests_mock.get('http://test.com', text='data')
    with tempfile.TemporaryDirectory() as directory_name:
        the_dir = pathlib.Path(directory_name)
        with open(download('http://test.com', the_dir)) as f:
            assert bs4.BeautifulSoup(f, 'lxml').get_text().strip() == 'data'
