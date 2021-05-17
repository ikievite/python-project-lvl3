

"""Test downloader module."""


import os
import pathlib
import tempfile
import logging
import pytest

import bs4

import requests_mock
from page_loader.downloader import (download, write_file,
                                    replace_local_urls, find_local_resources)
from page_loader.network_operations import format_url, HTML_EXTENSION

logger = logging.getLogger(__name__)

test_urls = [
    ('https://ru.hexlet.io/courses', HTML_EXTENSION, 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png', '', 'ru-hexlet-io-assets-professions-nodejs.png'),
    ('https://site.com/blog/about/assets/styles.css', '', 'site-com-blog-about-assets-styles.css'),
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


@pytest.mark.skip(reason='temp')
def test_download_check_content(requests_mock):
    requests_mock.get('http://test.com', text='data')
    with tempfile.TemporaryDirectory() as directory_name:
        the_dir = pathlib.Path(directory_name)
        with open(download('http://test.com', the_dir)) as f:
            assert bs4.BeautifulSoup(f, 'lxml').get_text().strip() == 'data'


expected_local_resources = [
    '/blog/about/assets/styles.css',
    '/blog/about',
    '/photos/me.jpg',
    'https://site.com/assets/scripts.js',
]


def test_find_local_recources():
    with open('tests/fixtures/site_com_content.txt') as content:
        page_content = content.read()
    local_resources = find_local_resources(page_content, 'https://site.com/blog/about')
    assert sorted(local_resources) == sorted(expected_local_resources)


def test_replace_local_urls():
    with open('tests/fixtures/site_com_content.txt') as content:
        with open('tests/fixtures/site_com_with_replaced_urls.txt') as result:
            page_content = content.read()
            expected = result.read()
            page_replaced = replace_local_urls(page_content, 'https://site.com/blog/about', expected_local_resources, 'site-com-blog-about_files')
    assert page_replaced == expected
