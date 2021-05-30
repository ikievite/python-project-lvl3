

"""Module that works with network."""


import logging
import os
import re
from urllib.parse import urlsplit

import requests

from page_loader.errors import RequestError

logger = logging.getLogger(__name__)

DELIMITER = '-'
HTML_EXTENSION = '.html'


def format_dirname(urlpath, suffix):
    """Format an url path.

    Args:
        urlpath: url
        suffix: suffix for name

    Returns:
        formatted directory name
    """
    splitted = urlsplit(urlpath)
    netloc = splitted.netloc.replace('.', DELIMITER)
    netpath = splitted.path.rstrip('/')
    netpath = re.sub('[^a-zA-Z0-9]', DELIMITER, netpath)
    return netloc + netpath + suffix


def format_filename(url, suffix=''):
    """Format an url path.

    Args:
        url: url
        suffix: suffix for name

    Returns:
        formatted url
    """
    splitted = urlsplit(url)
    netloc = splitted.netloc.replace('.', DELIMITER)
    netpath = splitted.path.rstrip('/')
    extention = os.path.splitext(netpath)[-1]
    netpath = netpath.replace(extention, '')
    netpath = re.sub('[^a-zA-Z0-9]', DELIMITER, netpath)
    formatted = netloc + netpath + suffix
    if extention:
        return '{0}{1}'.format(formatted, extention)
    if suffix:
        return formatted
    return formatted + HTML_EXTENSION


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


def get_content(url):
    """Download file.

    Args:
        url:url

    Returns:
        content

    Raises:
        RequestError: if there is a network problem
    """
    try:  # noqa: WPS229 # too long ``try`` body length
        logger.debug('Getting content from url {0}'.format(
            url,
        ))
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:  # noqa: WPS111 # too short name
        raise RequestError from e
