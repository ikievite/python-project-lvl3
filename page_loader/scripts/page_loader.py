

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
        print(page_content)  # noqa: WPS421 # ignore warning about print
    except AppInternalError as e:  # noqa: WPS111 # ignore warning about too short name
        print('Exception: {0}'.format(str(e)))  # noqa: WPS421 # ignore warning about print
    sys.exit(os.EX_OK)


if __name__ == '__main__':
    main()
