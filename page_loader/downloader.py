

"""Module downloads web page."""


import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from page_loader.file_operations import mkdir, mkpath, write_file, write_page
from page_loader.network_operations import HTML_EXTENSION, format_url, get_content, is_local

logger = logging.getLogger(__name__)

BS4_FORMATTER = 'html5'
BS4_PARSER = 'html.parser'
DIRECTORY_TRAILER = '_files'
TAGS = {'img': 'src', 'script': 'src', 'link': 'href'}  # noqa: WPS407 # mutable module constant


def find_local_resources(page_content, url):  # noqa: WPS210 # too many vars
    """Find, replace links to images.

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
        resource_filepath = mkpath(directory_name, urljoin(url, resource))
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
        resource_filepath = mkpath(directory_path, resource_full_url)
        write_file(resource_full_url, resource_filepath)


def download(url, output_dir):  # noqa: WPS210 # too many local variables
    """Download a web page.

    Args:
        url: url path
        output_dir: path to directory

    Returns:
        filepath to saved web page
    """
    logger.debug('Getting web page content for url {0}'.format(url))

    response = get_content(url).text

    local_resources = find_local_resources(response, url)

    directory_name = format_url(url, DIRECTORY_TRAILER)

    saved_page = replace_local_urls(response, url, local_resources, directory_name)

    page_filepath = mkpath(output_dir, url, HTML_EXTENSION)

    logger.debug('Saving web page with filepath: {0}'.format(page_filepath))
    write_page(saved_page, page_filepath)

    directory_path = mkpath(output_dir, url, DIRECTORY_TRAILER)

    logger.debug('Creating folder {0} for local resources: images, scripts...'.format(
        directory_path,
    ))
    mkdir(directory_path)

    download_local_resources(local_resources, url, directory_path)

    return page_filepath
