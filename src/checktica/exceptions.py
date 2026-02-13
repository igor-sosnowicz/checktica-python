"""Module with exceptions and errors."""


class CheckticaError(Exception):
    """Top-level error signaling that something went wrong around Checktica."""


class InvalidArgumentError(CheckticaError):
    """Raised if either name or value of the argument is invalid."""


class LimitExceededError(CheckticaError):
    """Raised if a number of API requests per interval of time exceeded a rate limit."""


class InvalidResponseError(CheckticaError):
    """Raised if the Checktica API returned incorrectly formatted response."""


class APIAccessError(CheckticaError):
    """Raised if there was either client of server issue make the API inaccessible."""
