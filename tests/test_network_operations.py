

"""Tests for network_operations module."""


import pytest
import logging
import requests
import requests_mock  # noqa: F401
from page_loader.network_operations import get_content, format_filename, HTML_EXTENSION
from page_loader.errors import RequestError


logger = logging.getLogger(__name__)

error_codes = [(404), (503)]


@pytest.mark.parametrize("code", error_codes)
def test_get_content_codes(requests_mock, code):  # noqa: F811
    requests_mock.get('http://test.com', status_code=code)
    with pytest.raises(RequestError):
        get_content('http://test.com')


def test_get_content_exception(requests_mock):  # noqa: F811
    requests_mock.get('http://test.com', exc=requests.exceptions.ConnectTimeout)
    with pytest.raises(RequestError):
        get_content('http://test.com')


test_filenames = [
    ('https://ru.hexlet.io/courses', HTML_EXTENSION, 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png', '', 'ru-hexlet-io-assets-professions-nodejs.png'),
    ('https://site.com/blog/about/assets/styles.css', '', 'site-com-blog-about-assets-styles.css'),
]


@pytest.mark.parametrize("url, extention, expected", test_filenames)
def test_format_filename(url, extention, expected):
    logger.debug('Testing format_url function')
    result = format_filename(url, extention)
    assert result == expected
