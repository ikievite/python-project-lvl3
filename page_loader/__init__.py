

"""Page Loader package."""


import logging

from page_loader.downloader import download

LOGFILE = 'logfile.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter(
    '{asctime} - {levelname} - {name} - {message}', datefmt='%H:%M:%S', style='{',
)

console.setFormatter(formatter)

logger.addHandler(console)

# File
logfile = logging.FileHandler(LOGFILE, 'w')
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '{asctime} - {levelname} - {name} - {message}',
    datefmt='%Y-%m-%d %H:%M:%S',  # noqa: WPS323 # ignore `%` string formatting
    style='{',
)
logfile.setFormatter(formatter)

logger.addHandler(logfile)


__all__ = (  # noqa: WPS410
    'download',
)
