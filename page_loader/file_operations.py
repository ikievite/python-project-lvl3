

"""Module works with files."""


import logging
import os

from page_loader.errors import FileError

logger = logging.getLogger(__name__)

CHUNK_SIZE = 100000


def write_file(link_content, filename):
    """Write file.

    Args:
        link_content: content
        filename: filename for file
    """
    logger.debug('Writing resource to file {0}'.format(
        filename,
    ))
    with open(filename, 'wb') as f:  # noqa: WPS111 # ignore warning about too short name
        for chunk in link_content.iter_content(CHUNK_SIZE):
            f.write(chunk)


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
