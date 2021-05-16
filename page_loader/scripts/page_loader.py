

"""Page loader."""


import os
import sys

from page_loader.args_parser import parse_arguments
from page_loader.downloader import download
from page_loader.errors import AppInternalError


def main():
    """Run main function."""
    args = parse_arguments()
    try:  # noqa: WPS229 # ignore warning about too long `try` body length
        page_content = download(args.url_path, args.output_dir)
        print('Page was successfully downloaded into {0}'.format(page_content))
        sys.exit(os.EX_OK)
    except AppInternalError as e:  # noqa: WPS111 # ignore warning about too short name
        print('Exception: {0}'.format(str(e)))
        sys.exit(1)


if __name__ == '__main__':
    main()
