

"""Module downloads web page."""


import logging
import os
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BS4_FORMATTER = 'html5'
CHUNK_SIZE = 100000
HTML_EXTENSION = '.html'
DIRECTORY_TRAILER = '_files'
DELIMITER = '-'
TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}  # noqa: WPS407 # mutable module constant


class AppInternalError(Exception):
    """A class to represent app error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


class RequestError(AppInternalError):
    """A class to represent download error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


def format_url(url, suffix):
    """Format an url path.

    Args:
        url: url
        suffix: suffix for name

    Returns:
        formatted url
    """
    splitted = urlsplit(url)
    netloc = splitted.netloc.replace('.', DELIMITER)
    netpath = splitted.path.rstrip('/').replace('/', DELIMITER)
    formatted = netloc + netpath
    return '{0}{1}'.format(formatted, suffix)


def download_file(url, filename):
    """Download file using `url`.

    Args:
        url: download link
        filename: filename for file
    """
    logger.debug('Downloading resource {0} with filepath and name {1}'.format(
        url,
        filename,
    ))
    response = requests.get(url)
    with open(filename, 'wb') as f:  # noqa: WPS111 # ignore warning about too short name
        for chunk in response.iter_content(CHUNK_SIZE):
            f.write(chunk)


def mkdir(directory_path):
    """Create directory.

    Args:
        directory_path: directory path
    """
    try:  # noqa: WPS229 # ignore warning about too long ``try`` body length
        logger.debug('Creating folder {0} for local resources: images, scripts...'.format(
            directory_path,
        ))
        os.mkdir(directory_path)
    except FileExistsError:
        print('The directory `{0}` was previously created'.format(  # noqa: WPS421
            directory_path,                                 # ignore warning about `print`
        ))


def is_local(resource_url, page_url):
    """Check is resource local.

    Args:
        resource_url: url to resource (image, script, link...)
        page_url: url to saved web page

    Returns:
        bool value
    """
    resource_netloc = urlsplit(resource_url).netloc
    page_netloc = urlsplit(page_url).netloc
    if resource_netloc == '':
        logger.debug('Resourse {0} is local'.format(resource_url))
        return True
    elif resource_netloc == page_netloc:
        logger.debug('Resourse {0} is local'.format(resource_url))
        return True
    logger.debug('Resourse {0} is non local'.format(resource_url))
    return False


def prepare_page(url, output_dir):  # noqa: WPS210, WPS231 # too many local variables
    """Find, replace links to images.         # function with too much cognitive complexity.

    Args:
        url: url, link to page
        output_dir: output_dir for saved page

    Returns:
        tag soup

    Raises:
        RequestError: if there is a network problem
    """
    try:  # noqa: WPS229 # too long ``try`` body length: 2 > 1
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:  # noqa: WPS111 # too short name
        raise RequestError(e)

    directory_name = format_url(url, DIRECTORY_TRAILER)
    directory_path = os.path.join(output_dir, directory_name)
    mkdir(directory_path)

    soup = BeautifulSoup(response.text, 'lxml')

    for tag, attr in TAGS.items():
        for resource in soup.find_all(tag):
            resource_src_url = resource.get(attr)
            if resource_src_url and is_local(resource_src_url, url):
                resource_full_url = urljoin(url, resource_src_url)
                logger.debug('{0} is full url for resource {1}'.format(
                    resource_full_url,
                    resource_src_url,
                ))
                resource_filename = format_url(resource_full_url, '')
                resource_filepath = os.path.join(
                    output_dir,
                    directory_name,
                    resource_filename,
                )
                download_file(resource_full_url, resource_filepath)
                resource_local_filepath = os.path.join(
                    directory_name,
                    resource_filename,
                )
                logger.debug('Replacing url from {0} to {1}'.format(
                    resource_src_url,
                    resource_local_filepath,
                ))
                if tag == 'link':
                    soup.find(href=resource_src_url)[attr] = resource_local_filepath
                elif tag == 'script' or tag == 'img':  # noqa: WPS514 # implicit `in` condition
                    soup.find(src=resource_src_url)[attr] = resource_local_filepath
    return soup


def download(url, output_dir):
    """Download a web page.

    Args:
        url: url path
        output_dir: path to directory

    Returns:
        filepath to saved web page
    """
    page_name = format_url(url, HTML_EXTENSION)

    page_filepath = os.path.join(output_dir, page_name)

    saved_page = prepare_page(url, output_dir)

    logger.debug('Saving web page with filepath: {0}'.format(page_filepath))
    with open(page_filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
        f.write(str(saved_page.prettify(formatter=BS4_FORMATTER)))

    return page_filepath
