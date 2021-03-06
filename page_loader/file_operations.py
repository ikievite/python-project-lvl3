

"""Module with helpers func."""


import logging
import os

import requests
from progress.counter import Stack

from page_loader.errors import FileError, RequestError

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024
PROGRESS_COLOR = 'green'


class FancyPie(Stack):
    """Class represents `pie` progress."""

    phases = ('○', '◔', '◑', '◕', '●')

    def update(self):
        """Update `pie`."""
        nphases = len(self.phases)
        i = min(nphases - 1, int(self.progress * nphases))
        message = self.message % self
        pie = self.phases[i]
        line = '  {0} {1}'.format(pie, message)
        self.writeln(line)


def download_file(url, filename):  # noqa: WPS210 # too many local variables
    """Download file.

    Args:
        url: url
        filename: filename

    Returns:
        download file
    """
    logger.debug('Writing resource {0} to file {1}'.format(
        url,
        filename,
    ))
    try:  # noqa: WPS229 # ignore warning about too long ``try`` body length
        link_content = requests.get(url, stream=True)
        link_content.raise_for_status()
    except requests.exceptions.RequestException as req_err:
        logger.warning(RequestError(req_err))
    with open(filename, 'wb') as f:
        total_length = link_content.headers.get('content-length')
        if not total_length:
            return f.write(link_content.content)
        chunks = int(total_length) / CHUNK_SIZE
        with FancyPie(url, max=chunks) as progress:
            for chunk in link_content.iter_content(CHUNK_SIZE):
                f.write(chunk)
                progress.next()  # noqa: B305


def save_page(page_content, filepath):
    """Save web page to filesystem.

    Args:
        page_content: content
        filepath: filepath

    Raises:
        FileError: if there a problem with write permissions
    """
    try:
        with open(filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
            f.write(page_content)
    except OSError as e:
        raise FileError('I/O failure occured while saving {0}'.format(filepath)) from e


def mkdir(directory_path):
    """Create directory.

    Args:
        directory_path: directory path

    Raises:
        FileError: if there a problem with files.
    """
    try:
        os.mkdir(directory_path)
    except FileExistsError:
        print('The directory `{0}` was previously created'.format(  # noqa: WPS421
            directory_path,                                 # ignore warning about `print`
        ))
    except OSError as e:
        raise FileError('I/O failure occured while creating {0}'.format(directory_path)) from e
