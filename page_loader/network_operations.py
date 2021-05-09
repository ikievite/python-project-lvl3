

"""Module works with network."""


import logging

import requests

from page_loader.errors import RequestError

logger = logging.getLogger(__name__)


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
        return response
    except requests.exceptions.RequestException as e:  # noqa: WPS111 # too short name
        raise RequestError(e)
