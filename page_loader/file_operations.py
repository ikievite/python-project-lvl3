

"""Module works with files."""


import logging
import os

import requests
from progress.colors import color
from progress.counter import Stack

from page_loader.errors import FileError, RequestError

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024


class FancyPie(Stack):  # noqa: D101 # ignore warning about missing docstring in public class
    phases = ('○', '◔', '◑', '◕', '●')
    color = None

    def update(self):  # noqa: D102 # ignore warning about missing docstring in public method
        nphases = len(self.phases)
        i = min(nphases - 1, int(self.progress * nphases))  # noqa: WPS111 # too short name
        message = self.message % self
        pie = color(self.phases[i], fg=self.color)
        line = ''.join(['  {0} {1}'.format(pie, message)])
        self.writeln(line)


def write_file(url, filename):
    """Write file.

    Args:
        url: url
        filename: filename for file
    """
    logger.debug('Writing resource {0} to file {1}'.format(
        url,
        filename,
    ))
    try:
        link_content = requests.get(url, stream=True)
        link_content.raise_for_status()
        total_length = link_content.headers.get('content-length')
        with open(filename, 'wb') as f:  # noqa: WPS111 # ignore warning about too short name
            if total_length:
                with FancyPie(url, max=int(total_length)/CHUNK_SIZE, color='green') as progress:
                    for chunk in link_content.iter_content(CHUNK_SIZE):
                        f.write(chunk)  # noqa: WPS220 # too deep nesting: 24 > 20
                        progress.next()  # noqa: B305, WPS220
            else:
                f.write(link_content.content)
    except requests.exceptions.RequestException as e:  # noqa: WPS111 # too short name
        logger.warning(RequestError(e))


def mkdir(directory_path):
    """Create directory.

    Args:
        directory_path: directory path

    Raises:
        FileError: if there a problem with files.
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
    except FileNotFoundError as e:  # noqa: WPS111 # ignore warning - too short name: e < 2
        raise FileError('No such output {0} directory'.format(directory_path)) from e
    except PermissionError as e:  # noqa: WPS111 # ignore warning - too short name: e < 2
        raise FileError('No write permissions for {0} directory'.format(directory_path)) from e
