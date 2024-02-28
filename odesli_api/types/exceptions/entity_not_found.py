from .api_exception import APIException


class EntityNotFound(APIException):
    """
    Exception raised when an entity is not found.
    """

    def __init__(self):
        """
        Initializes EntityNotFound with status code 404 and default message.
        """
        super().__init__(status_code=404, message="Entity not found.")


__all__ = ("EntityNotFound",)
