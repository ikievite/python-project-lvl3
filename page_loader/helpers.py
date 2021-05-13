

"""Module with helpers func."""


import logging
import os

import requests
from progress.colors import color
from progress.counter import Stack

from page_loader.errors import FileError, RequestError

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024
PROGRESS_COLOR = 'green'


class FancyPie(Stack):
    """Class represents `pie` progress."""

    phases = ('○', '◔', '◑', '◕', '●')
    color = None

    def update(self):
        """Update `pie`."""
        nphases = len(self.phases)
        i = min(nphases - 1, int(self.progress * nphases))
        message = self.message % self
        pie = color(self.phases[i], fg=self.color)
        line = ''.join(['  {0} {1}'.format(pie, message)])
        self.writeln(line)


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


def write_file(url, filename):  # noqa: WPS210 # too many local variables
    """Write file.

    Args:
        url: url
        filename: filename
    """
    logger.debug('Writing resource {0} to file {1}'.format(
        url,
        filename,
    ))
    try:  # noqa: WPS229 # ignore warning about too long ``try`` body length
        with requests.get(url, stream=True) as link_content, open(filename, 'wb') as f:
            link_content.raise_for_status()
            total_length = link_content.headers.get('content-length')
            if total_length:
                chunks = int(total_length)/CHUNK_SIZE
                with FancyPie(url, max=chunks, color=PROGRESS_COLOR) as progress:
                    for chunk in link_content.iter_content(CHUNK_SIZE):
                        f.write(chunk)  # noqa: WPS220 # too deep nesting
                        progress.next()  # noqa: B305, WPS220
            else:
                f.write(link_content.content)
    except requests.exceptions.RequestException as req_err:
        logger.warning(RequestError(req_err))


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
    except FileNotFoundError as e:
        raise FileError('No such output {0} directory'.format(directory_path)) from e
    except PermissionError as e:
        raise FileError('No write permissions for {0} directory'.format(directory_path)) from e
