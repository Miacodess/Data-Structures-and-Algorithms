"""Custom errors used across the support desk."""


class DuplicateRequestError(Exception):
    """Raised when a request ID has already been used."""