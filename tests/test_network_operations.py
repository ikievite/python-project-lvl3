

"""Tests for network_operations module."""


import pytest
import requests
import requests_mock
from page_loader.helpers import get_content
from page_loader.errors import RequestError


test_data = [
    (404, '404 Client Error'),
    (503, '503 Server Error'),
]

@pytest.mark.parametrize("code,description", test_data)
def test_get_content_codes(requests_mock, code, description):
    requests_mock.get('http://test.com', status_code=code)
    with pytest.raises(RequestError, match=description) as exc_info:
        get_content('http://test.com')


def test_get_content_exception(requests_mock):
    requests_mock.get('http://test.com', exc=requests.exceptions.ConnectTimeout)
    with pytest.raises(RequestError) as exc_info:
        get_content('http://test.com')
