class InvalidArgumentException(Exception):
    """Used when the API request contains invalid arguments."""
    pass


class InsufficientDataException(Exception):
    """Used when the data gathered by the API is insufficient to properly serve the request"""
    pass


