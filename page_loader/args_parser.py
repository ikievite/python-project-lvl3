

"""Module parses arguments."""


import argparse
import logging
import os

logger = logging.getLogger(__name__)


def parse_arguments():
    """Create parser and adds arguments.

    Returns:
        an object with attributes.
    """
    parser = argparse.ArgumentParser(description='Description: Page Loader.')
    parser.add_argument('url_path')
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        dest='output_dir',
        help='set output directory (default: is your current working directory)',
    )
    return parser.parse_args()
