

"""Test downloader module."""


import requests_mock
import tempfile
import pathlib
from page_loader.downloader import replace_local_urls, find_local_resources, download


expected_local_resources = [
    '/blog/about/assets/styles.css',
    '/blog/about',
    '/photos/me.jpg',
    'https://site.com/assets/scripts.js',
]


def test_find_local_recources():
    with open('tests/fixtures/site_com_content.txt') as content:
        page_content = content.read()
    local_resources = find_local_resources(page_content, 'https://site.com/blog/about')
    assert sorted(local_resources) == sorted(expected_local_resources)


def test_replace_local_urls():
    with open('tests/fixtures/site_com_content.txt') as content:
        with open('tests/fixtures/site_com_with_replaced_urls.txt') as result:
            page_content = content.read()
            expected = result.read()
            page_replaced = replace_local_urls(
                page_content,
                'https://site.com/blog/about',
                expected_local_resources,
                'site-com-blog-about_files'
            )
    assert page_replaced == expected


def test_download():
    with open('tests/fixtures/site_com_content.txt') as f:
        web_page = f.read()
    with open('tests/fixtures/styles.css', 'rb') as f:
        styles = f.read()
    with open('tests/fixtures/me.jpg', 'rb') as f:
        me_jpeg = f.read()
    with open('tests/fixtures/scripts.js', 'rb') as f:
        scripts = f.read()
    with requests_mock.Mocker() as mock:
        mock.get('http://site.com/blog/about', text=web_page)
        mock.get('http://site.com/blog/about/assets/styles.css', content=styles)
        mock.get('http://site.com/photos/me.jpg', content=me_jpeg)
        mock.get('https://site.com/assets/scripts.js', content=scripts)
        with tempfile.TemporaryDirectory() as directory_name:
            the_dir = pathlib.Path(directory_name)
            download('http://site.com/blog/about', the_dir)
