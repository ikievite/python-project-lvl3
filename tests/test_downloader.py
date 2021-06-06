

"""Test downloader module."""


import pathlib
from bs4 import BeautifulSoup
from page_loader.downloader import replace_local_urls, find_local_resources, download, BS4_PARSER


expected_local_resources = [
    '/blog/about/assets/styles.css',
    '/blog/about',
    '/photos/me.jpg',
    'https://site.com/assets/scripts.js',
]


def test_find_local_recources():
    with open('tests/fixtures/site_com_content.txt') as content:
        page_content = content.read()
    soup = BeautifulSoup(page_content, BS4_PARSER)
    local_resources = find_local_resources(soup, 'https://site.com/blog/about')
    assert sorted(local_resources) == sorted(expected_local_resources)


def test_replace_local_urls():
    with open('tests/fixtures/site_com_content.txt') as content:
        with open('tests/fixtures/site_com_with_replaced_urls.txt') as result:
            soup = BeautifulSoup(content, BS4_PARSER)
            expected = result.read()
            page_replaced = replace_local_urls(
                soup,
                'https://site.com/blog/about',
                expected_local_resources,
                'site-com-blog-about_files'
            )
    assert page_replaced == expected


def test_download(requests_mock, tmpdir):
    with open('tests/fixtures/site_com_content.txt') as f:
        web_page = f.read()
    with open('tests/fixtures/styles.css', 'rb') as f:
        styles = f.read()
    with open('tests/fixtures/me.jpg', 'rb') as f:
        me_jpeg = f.read()
    with open('tests/fixtures/scripts.js', 'rb') as f:
        scripts = f.read()
    requests_mock.get('http://site.com/blog/about', text=web_page)
    requests_mock.get('http://site.com/blog/about/assets/styles.css', content=styles)
    requests_mock.get('http://site.com/photos/me.jpg', content=me_jpeg)
    requests_mock.get('https://site.com/assets/scripts.js', content=scripts)
    directory_name = str(tmpdir)
    downloaded_page = download('http://site.com/blog/about', directory_name)

    with open(downloaded_page) as f:
        saved_page = f.read()
    with open('tests/fixtures/site_com_with_replaced_urls.txt') as f:
        expected_saved_page = f.read()
    assert saved_page == expected_saved_page

    with open(pathlib.Path(directory_name, 'site-com-blog-about_files/site-com-blog-about-assets-styles.css')) as f:
        saved_styles = f.read()
    with open('tests/fixtures/styles.css') as f:
        styles = f.read()
    assert saved_styles == styles

    with open(pathlib.Path(directory_name, 'site-com-blog-about_files/site-com-assets-scripts.js')) as f:
        saved_scripts = f.read()
    with open('tests/fixtures/scripts.js') as f:
        scripts = f.read()
    assert saved_scripts == scripts

    with open(pathlib.Path(directory_name, 'site-com-blog-about_files/site-com-photos-me.jpg'), 'rb') as f:
        saved_photo = f.read()
    assert saved_photo == me_jpeg
