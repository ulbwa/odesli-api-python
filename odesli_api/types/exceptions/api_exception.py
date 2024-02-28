from typing import Optional


class APIException(Exception):
    """
    Exception class for API errors.

    :ivar status_code: The status code of the API response.
    :ivar message: Optional. A message describing the exception.
    """

    def __init__(self, status_code: int, message: Optional[str] = None):
        """
        Initializes APIException with status code and optional message.

        :param status_code: The status code of the API response.
        :param message: Optional. A message describing the exception.
        """
        self.status_code = status_code
        self.message = (
            "{} ({})".format(message, status_code) if message else str(status_code)
        )
        super().__init__(self.message)


__all__ = ("APIException",)
