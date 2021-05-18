

"""Tests for page-loader package."""


import subprocess
import tempfile


def test_error_exit_code():
    with tempfile.TemporaryDirectory() as tmpdirname:
        INVALID_BASE_URL = ['poetry', 'run', 'page-loader', '-o', tmpdirname, 'http://badsite']
        process = subprocess.run(INVALID_BASE_URL, stdout=subprocess.DEVNULL)
        assert process.returncode != 0
