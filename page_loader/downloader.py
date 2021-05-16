

"""Module downloads web page."""


import logging
import os
import pathlib
import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

from page_loader.helpers import get_content, mkdir, write_file

logger = logging.getLogger(__name__)

BS4_FORMATTER = 'html5'
BS4_PARSER = 'html.parser'
HTML_EXTENSION = '.html'
DIRECTORY_TRAILER = '_files'
DELIMITER = '-'
TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}  # noqa: WPS407 # mutable module constant


def format_url(url, suffix):
    """Format an url path.

    Args:
        url: url
        suffix: suffix for name

    Returns:
        formatted url
    """
    splitted = urlsplit(url)
    netloc = splitted.netloc.replace('.', DELIMITER)
    netpath = splitted.path.rstrip('/')
    extention = pathlib.Path(netpath).suffix.lower()
    netpath = netpath.replace(extention, '')
    netpath = re.sub('[^a-zA-Z0-9]', DELIMITER, netpath)
    formatted = netloc + netpath + suffix
    if extention:
        return '{0}{1}'.format(formatted, extention)
    if suffix:
        return formatted
    return formatted + HTML_EXTENSION


def is_local(resource_url, page_url):
    """Check is resource local.

    Args:
        resource_url: url to resource (image, script, link...)
        page_url: url to saved web page

    Returns:
        bool value
    """
    resource_netloc = urlsplit(resource_url).netloc
    page_netloc = urlsplit(page_url).netloc
    if resource_netloc == '':
        logger.debug('Resourse {0} is local'.format(resource_url))
        return True
    elif resource_netloc == page_netloc:
        logger.debug('Resourse {0} is local'.format(resource_url))
        return True
    logger.debug('Resourse {0} is non local'.format(resource_url))
    return False


def find_local_resources(page_content, url):  # noqa: WPS210, WPS231 # too many vars
    """Find, replace links to images.         # function with too much cognitive complexity.

    Args:
        page_content: content
        url: link to page

    Returns:
        page with replaced local urls
    """
    soup = BeautifulSoup(page_content, BS4_PARSER)
    local_resources = []
    for tag, attr in TAGS.items():
        for resource in soup.find_all(tag):
            resource_src_url = resource.get(attr)
            if resource_src_url and is_local(resource_src_url, url):
                local_resources.append(resource_src_url)
    return local_resources


def replace_local_urls(page_content, url, local_resources, directory_name):
    """Find, replace links to local resources.

    Args:
        page_content: content
        url: url
        local_resources: list with urls to local resources
        directory_name: dir for local resources

    Returns:
        page with replaced local urls
    """
    soup = BeautifulSoup(page_content, BS4_PARSER)

    for resource in local_resources:
        resource_full_url = urljoin(url, resource)
        resource_filename = format_url(resource_full_url, '')
        resource_filepath = os.path.join(
            directory_name,
            resource_filename,
        )
        if soup.find(href=resource):
            soup.find(href=resource)['href'] = resource_filepath
        elif soup.find(src=resource):
            soup.find(src=resource)['src'] = resource_filepath
    return str(soup.prettify(formatter=BS4_FORMATTER))


def download_local_resources(resources, url, directory_path):
    """Download local resources for saved web page.

    Args:
        resources: list with local resources
        url: url
        directory_path: directory_path
    """
    for resource in resources:
        resource_full_url = urljoin(url, resource)
        resource_filename = format_url(resource_full_url, '')
        resource_filepath = os.path.join(
            directory_path,
            resource_filename,
        )
        write_file(resource_full_url, resource_filepath)


def download(url, output_dir):  # noqa: WPS210 # too many local variables
    """Download a web page.

    Args:
        url: url path
        output_dir: path to directory

    Returns:
        filepath to saved web page
    """
    logging.debug('Getting web page content for url {0}'.format(url))

    page_name = format_url(url, HTML_EXTENSION)
    page_filepath = os.path.join(output_dir, page_name)

    response = get_content(url).text

    directory_name = format_url(url, DIRECTORY_TRAILER)
    directory_path = os.path.join(output_dir, directory_name)

    logging.debug('Creating folder {0} for local resources: images, scripts...'.format(
        directory_path,
    ))
    mkdir(directory_path)

    local_resources = find_local_resources(response, url)
    saved_page = replace_local_urls(response, url, local_resources, directory_name)

    logger.debug('Saving web page with filepath: {0}'.format(page_filepath))
    with open(page_filepath, 'w') as f:  # noqa: WPS111 # ignore warning about too short name
        f.write(saved_page)

    download_local_resources(local_resources, url, directory_path)

    return page_filepath
