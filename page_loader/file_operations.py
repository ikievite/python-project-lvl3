

"""Module with helpers func."""


import logging
import os
import pathlib

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
                chunks = int(total_length) / CHUNK_SIZE
                with FancyPie(url, max=chunks) as progress:
                    for chunk in link_content.iter_content(CHUNK_SIZE):
                        f.write(chunk)  # noqa: WPS220 # too deep nesting
                        progress.next()  # noqa: B305, WPS220
            else:
                f.write(link_content.content)
    except requests.exceptions.RequestException as req_err:
        logger.warning(RequestError(req_err))


def write_page(page_content, filepath):
    """Write web page to filesystem.

    Args:
        page_content: content
        filepath: filepath

    Raises:
        FileError: if there a problem with write permissions
    """
    try:
        with open(filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
            f.write(page_content)
    except FileNotFoundError as e:
        raise FileError('No such output `{0}` directory'.format(
            pathlib.Path(filepath).parent,
        )) from e
    except PermissionError as e:
        raise FileError('No write permissions for saving `{0}`'.format(filepath)) from e
    except OSError as e:
        raise FileError('Disk full. Can`t save {0}'.format(filepath)) from e


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
