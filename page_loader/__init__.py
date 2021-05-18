

"""Page Loader package."""


import logging

from page_loader.downloader import download

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


__all__ = (  # noqa: WPS410
    'download',
)
