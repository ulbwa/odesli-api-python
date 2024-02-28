from .api_exception import APIException


class TooManyRequests(APIException):
    """
    Exception raised when there are too many requests made to the API.
    """

    def __init__(self):
        """
        Initializes TooManyRequests with status code 429 and default message.
        """
        super().__init__(
            status_code=429,
            message="Too many requests.",
        )


__all__ = ("TooManyRequests",)
