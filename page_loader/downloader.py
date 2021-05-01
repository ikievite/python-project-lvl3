

"""Module downloads web page."""


import os

import requests

CHUNK_SIZE = 100000
HTML_EXTENSION = 'html'


class RequestError(Exception):
    """A class to represent download error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


def format_url(path):
    """Format an url path.

    Args:
        path: url path

    Returns:
        formatted url
    """
    path = path.split('//')[-1]
    path = path.replace('/', '-').replace('.', '-')
    return '{path}.{extension}'.format(path=path, extension=HTML_EXTENSION)


def download(url_path, output_dir):
    """Download a web page.

    Args:
        url_path: url path
        output_dir: path to directory

    Returns:
        formatted url path
    """
    res = requests.get(url_path)

    formatted_url = format_url(url_path)

    formatted_path = os.path.join(output_dir, formatted_url)

    with open(formatted_path, 'wb') as f:  # noqa: WPS111 # ignore warning about too short name
        for chunk in res.iter_content(CHUNK_SIZE):
            f.write(chunk)

    return formatted_path
