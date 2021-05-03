

"""Module downloads web page."""


import os

import requests
from bs4 import BeautifulSoup

CHUNK_SIZE = 100000
HTML_EXTENSION = '.html'
DIRECTORY_TRAILER = '_files'


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
    path = path.split('//')[-1]
    path = path.replace('/', '-').replace('.', '-')
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


def mkdir(dir_name, output_dir):
    """Create directory.

    Args:
        dir_name: dir_name
        output_dir: output_dir
    """
    directory_path = os.path.join(output_dir, dir_name)
    try:
        os.mkdir(directory_path)
    except FileExistsError:
        print('The directory `{0}` was previously created'.format(  # noqa: WPS421
            directory_path,                                 # ignore warning about `print`
        ))


def prepare_page(url, output_dir):  # noqa: WPS210 # ignore warning about too many local variables
    """Find, replace links to images.

    Args:
        url: url path
        output_dir: output_dir

    Returns:
        tag soup
    """
    response = requests.get(url)

    directory_name = format_url(url, DIRECTORY_TRAILER)

    mkdir(directory_name, output_dir)

    soup = BeautifulSoup(response.text, 'lxml')

    for image in soup.find_all('img'):
        image_src_url = image['src']
        image_full_url = os.path.join(url, os.path.normpath(image_src_url))
        image_path = os.path.join(directory_name, format_url(image_full_url, ''))
        download_file(image_full_url, image_path)
        soup.find(src=image_src_url)['src'] = image_path
    return soup


def download(url_path, output_dir):
    """Download a web page.

    Args:
        url_path: url path
        output_dir: path to directory

    Returns:
        formatted url path
    """
    page_name = format_url(url_path, HTML_EXTENSION)

    page_filepath = os.path.join(output_dir, page_name)

    saved_page = prepare_page(url_path, output_dir)

    with open(page_filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
        f.write(str(saved_page.prettify(formatter='html5')))

    return page_filepath
