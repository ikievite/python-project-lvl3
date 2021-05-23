

"""Tests for file_operations module."""


import logging
import os
import pathlib
import tempfile
import urllib

import pytest
import requests_mock

from page_loader.errors import FileError
from page_loader.file_operations import mkdir, write_file, write_page

logger = logging.getLogger(__name__)

DIRECTORY = 'tests/fixtures/OUTPUT_DIRECTORY'


def test_mkdir_exists():
    mkdir(DIRECTORY)
    assert True == os.path.exists(DIRECTORY)


test_directories = [
    ('tests/fixtures/NOT_EXISTS/output'),
    ('/root/no_rights/output'),
]


@pytest.mark.parametrize("directory", test_directories)
def test_mkdir_exception(directory):
    with pytest.raises(FileError) as exc_info:
        mkdir(directory)


test_write_page_data = [
    ('tests/fixtures/NOT_EXISTS/output', 'No such output `tests/fixtures/NOT_EXISTS/output` directory'),
    ('/root/no_rights/output', 'No write permissions for saving `/root/no_rights/output/test.html`')
]


@pytest.mark.parametrize("directory,error_msg", test_write_page_data)
def test_write_page_exc(directory, error_msg):
    with pytest.raises(FileError) as exc_info:
        write_page('test_content', os.path.join(directory, 'test.html'))
    exception_msg = exc_info.value.args[0]
    expected = error_msg
    assert exception_msg == expected


def test_write_page():
    with open('tests/fixtures/site_com_content.txt') as web_page, \
            tempfile.TemporaryDirectory() as directory_name:
        page_content = web_page.read()
        page_filepath = urllib.parse.urljoin(directory_name, 'example.html')
    write_page(page_content, page_filepath)
    with open(page_filepath) as saved_file:
        saved_content = saved_file.read()
    assert page_content == saved_content


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
