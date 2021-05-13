

"""Tests for file_operations module."""


import pytest
from page_loader.helpers import mkdir
from page_loader.errors import FileError


DIRECTORY = 'tests/fixtures/OUTPUT_DIRECTORY'

test_data = [
    ('tests/fixtures/NOT_EXISTS/output', 'No such output {0} directory'),
    ('/root/no_rights/output', 'No write permissions for {0} directory')
]


def test_mkdir_exists(capsys):
    mkdir(DIRECTORY)
    out, err = capsys.readouterr()
    assert out.strip() == 'The directory `{0}` was previously created'.format(DIRECTORY)


@pytest.mark.parametrize("directory,error_msg", test_data)
def test_mkdir_not_found(directory, error_msg):
    with pytest.raises(FileError) as exc_info:
        mkdir(directory)
    exception_msg = exc_info.value.args[0]
    expected = error_msg.format(directory)
    assert exception_msg == expected
