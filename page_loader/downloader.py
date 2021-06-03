

"""Module downloads web page."""


import logging
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from page_loader.file_operations import download_file, mkdir, save_page
from page_loader.network_operations import (
    format_filename,
    format_resource_dirname,
    get_content,
    is_local,
)

BS4_FORMATTER = 'html5'
BS4_PARSER = 'html.parser'
DIRECTORY_TRAILER = '_files'
TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}  # noqa: WPS407 # mutable module constant
logger = logging.getLogger(__name__)


def find_local_resources(soup, url):
    """Find links to local resources.

    Args:
        soup: tag soup
        url: link to page

    Returns:
        list with local resources
    """
    local_resources = []
    for resource in soup.find_all(TAGS):
        attr = TAGS.get(resource.name)
        resource_src_url = resource.get(attr)
        if resource_src_url and is_local(resource_src_url, url):
            local_resources.append(resource_src_url)
    return local_resources


def replace_local_urls(soup, url, local_resources, resource_dirname):
    """Replace links to local resources.

    Args:
        soup: tag soup
        url: url
        local_resources: list with urls to local resources
        resource_dirname: name of directory with local resources

    Returns:
        page with replaced local urls
    """
    for resource in soup.find_all(TAGS):
        attr = TAGS.get(resource.name)
        resource_src_url = resource.get(attr)
        if resource_src_url in local_resources:
            resource_filepath = os.path.join(
                resource_dirname,
                format_filename(urljoin(url, resource_src_url)),
            )
            resource[attr] = resource_filepath
    return str(soup.prettify(formatter=BS4_FORMATTER))


def download_resources(resources, url, dirpath):
    """Download resources for web page.

    Args:
        resources: list with resources
        url: url
        dirpath: path to directory with files/resources
    """
    for resource in resources:
        resource_full_url = urljoin(url, resource)
        resource_filepath = os.path.join(dirpath, format_filename(resource_full_url))
        download_file(resource_full_url, resource_filepath)


def download(url, output_dir):  # noqa: WPS210 # too many local variables
    """Download a web page.

    Args:
        url: url path
        output_dir: path to directory with saved web page

    Returns:
        filepath to saved web page
    """
    logger.debug('Getting web page content for url {0}'.format(url))

    page_content = get_content(url)

    soup = BeautifulSoup(page_content, BS4_PARSER)

    local_resources = find_local_resources(soup, url)

    resource_dirname = format_resource_dirname(url, DIRECTORY_TRAILER)

    modified_page = replace_local_urls(soup, url, local_resources, resource_dirname)

    page_filepath = os.path.join(output_dir, format_filename(url))

    logger.debug('Saving web page with filepath: {0}'.format(page_filepath))
    save_page(modified_page, page_filepath)

    resource_dirpath = os.path.join(output_dir, resource_dirname)

    logger.debug('Creating folder {0} for local resources: images, scripts...'.format(
        resource_dirpath,
    ))
    mkdir(resource_dirpath)

    download_resources(local_resources, url, resource_dirpath)

    return page_filepath
