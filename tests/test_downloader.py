

"""Test downloader module."""


from page_loader.downloader import format_url


def test_format_url():
    assert format_url('https://ru.hexlet.io/courses') == 'ru-hexlet-io-courses.html'
