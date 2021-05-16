

"""Tests for page-loader package."""


import subprocess
import pathlib
import tempfile

import bs4

import pytest
from page_loader.scripts.page_loader import download


@pytest.mark.skip(reason='deativate')
def test_download_check_content(requests_mock):
    requests_mock.get('http://test.com', text='data')
    with tempfile.TemporaryDirectory() as directory_name:
        the_dir = pathlib.Path(directory_name)
        with open(download('http://test.com', the_dir)) as f:
            assert bs4.BeautifulSoup(f, 'lxml').get_text().strip() == 'data'


def test_error_exit_code():
    with tempfile.TemporaryDirectory() as tmpdirname:
        INVALID_BASE_URL = ['poetry', 'run', 'page-loader', '-o', tmpdirname, 'http://badsite']
        process = subprocess.run(INVALID_BASE_URL, stdout=subprocess.DEVNULL)
        assert process.returncode != 0
