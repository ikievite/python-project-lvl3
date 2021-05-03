

"""Module downloads web page."""


import os
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

CHUNK_SIZE = 100000
HTML_EXTENSION = '.html'
DIRECTORY_TRAILER = '_files'
DELIMITER = '-'


class RequestError(Exception):
    """A class to represent download error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


def format_url(path, suffix):
    """Format an url path.

    Args:
        path: url path
        suffix: suffix for name

    Returns:
        formatted url
    """
    splitted = urlsplit(path)
    netloc = splitted.netloc.replace('.', DELIMITER)
    netpath = splitted.path.rstrip('/').replace('/', DELIMITER)
    path = netloc + netpath
    return '{path}{extension}'.format(path=path, extension=suffix)


def download_file(url, filename):
    """Download file using `url`.

    Args:
        url: download link
        filename: filename for file
    """
    response = requests.get(url)
    with open(filename, 'wb') as f:  # noqa: WPS111 # ignore warning about too short name
        for chunk in response.iter_content(CHUNK_SIZE):
            f.write(chunk)


def mkdir(directory_path):
    """Create directory.

    Args:
        directory_path: directory path
    """
    try:
        os.mkdir(directory_path)
    except FileExistsError:
        print('The directory `{0}` was previously created'.format(  # noqa: WPS421
            directory_path,                                 # ignore warning about `print`
        ))


def prepare_page(url, output_dir):  # noqa: WPS210 # ignore warning about too many local variables
    """Find, replace links to images.

    Args:
        url: url, link to page
        output_dir: output_dir for saved page

    Returns:
        tag soup
    """
    response = requests.get(url)

    directory_name = format_url(url, DIRECTORY_TRAILER)
    directory_path = os.path.join(output_dir, directory_name)
    mkdir(directory_path)

    soup = BeautifulSoup(response.text, 'lxml')

    for image in soup.find_all('img'):
        image_src_url = image['src']
        image_full_url = urljoin(url, image_src_url)
        image_filepath = os.path.join(output_dir, directory_name, format_url(image_full_url, ''))
        download_file(image_full_url, image_filepath)
        soup.find(src=image_src_url)['src'] = image_filepath
    return soup


def download(url, output_dir):
    """Download a web page.

    Args:
        url: url path
        output_dir: path to directory

    Returns:
        formatted url
    """
    page_name = format_url(url, HTML_EXTENSION)

    page_filepath = os.path.join(output_dir, page_name)

    saved_page = prepare_page(url, output_dir)

    with open(page_filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
        f.write(str(saved_page.prettify(formatter='html5')))

    return page_filepath
