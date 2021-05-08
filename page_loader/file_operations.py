

"""Module works with files."""


import logging
import os

import requests

logger = logging.getLogger(__name__)

CHUNK_SIZE = 100000


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
