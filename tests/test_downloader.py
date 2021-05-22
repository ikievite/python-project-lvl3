

"""Test downloader module."""


from page_loader.downloader import replace_local_urls, find_local_resources


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
