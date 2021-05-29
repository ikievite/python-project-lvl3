

"""Tests for file_operations module."""


import logging
import os
import pathlib
import tempfile
import urllib

import pytest
from page_loader.errors import FileError
from page_loader.file_operations import mkdir, download_file, save_page

logger = logging.getLogger(__name__)

DIRECTORY = 'tests/fixtures/OUTPUT_DIRECTORY'


def test_mkdir_exists():
    mkdir(DIRECTORY)
    assert True == os.path.exists(DIRECTORY)  # noqa: E712


test_directories = [
    ('tests/fixtures/NOT_EXISTS/output'),
    ('/root/no_rights/output'),
]


@pytest.mark.parametrize("directory", test_directories)
def test_mkdir_exception(directory):
    with pytest.raises(FileError):
        mkdir(directory)


test_dirs = [
    ('tests/fixtures/NOT_EXISTS/output'),
    ('/root/no_rights/output'),
]


@pytest.mark.parametrize("directory", test_dirs)
def test_save_page_exc(directory):
    with pytest.raises(FileError):
        save_page('test_content', os.path.join(directory, 'test.html'))


def test_save_page():
    with open('tests/fixtures/site_com_content.txt') as web_page, \
            tempfile.TemporaryDirectory() as directory_name:
        page_content = web_page.read()
        page_filepath = urllib.parse.urljoin(directory_name, 'example.html')
    save_page(page_content, page_filepath)
    with open(page_filepath) as saved_file:
        saved_content = saved_file.read()
    assert page_content == saved_content


def test_download_file(requests_mock, sample_file='tests/fixtures/original.original'):
    with open(sample_file, 'rb') as f:
        sample_file = f.read()
    dl_path = 'http://test.com/thefile.file'

    requests_mock.get(dl_path, content=sample_file)

    with tempfile.TemporaryDirectory() as directory_name:
        the_dir = pathlib.Path(directory_name)
        target_path = os.path.join(the_dir, 'test.file')
        download_file(dl_path, target_path)

        assert os.path.isfile(target_path)

        with open(target_path, 'rb') as f:
            assert f.read() == sample_file
