

"""Module stores known possible errors."""


class AppInternalError(Exception):
    """A class to represent app error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


class RequestError(AppInternalError):
    """A class to represent network error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body


class FileError(AppInternalError):
    """A class to represent file error."""

    pass  # noqa: WPS420, WPS604 # ignore wrong keyword: pass, incorrect node inside `class` body
