

"""Module stores known possible errors."""


class AppInternalError(Exception):
    """A class to represent app error."""

    pass


class RequestError(AppInternalError):
    """A class to represent network error."""

    pass


class FileError(AppInternalError):
    """A class to represent file error."""

    pass
