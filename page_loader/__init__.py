

"""Page Loader package."""


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

### stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter(
    '{asctime} - {levelname} - {name} - {message}', datefmt='%H:%M:%S', style='{',
)

console.setFormatter(formatter)

logger.addHandler(console)

### File
logfile = logging.FileHandler('logfile.log')
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '{asctime} - {levelname} - {name} - {message}', datefmt='%H:%M:%S', style='{',
)
logfile.setFormatter(formatter)

logger.addHandler(logfile)
