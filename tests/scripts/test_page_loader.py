

"""Tests for page-loader package."""


from page_loader.scripts.page_loader import main


def test_main():
    assert main() == 'Let\'s start.'
