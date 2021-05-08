

"""Module works with network."""


import logging

import requests

logger = logging.getLogger(__name__)


def get_content(url):
    """Download file.

    Args:
        url:url

    Returns:
        content
    """
    logger.debug('Getting content from url {0}'.format(
        url,
    ))
    return requests.get(url)
