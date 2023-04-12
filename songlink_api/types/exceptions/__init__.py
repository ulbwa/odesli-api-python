from typing import Optional


class APIException(Exception):
    def __init__(self, status_code: int, message: Optional[str] = None):
        self.status_code = status_code
        self.message = (
            "{} ({})".format(message, status_code)
            if message is not None
            else str(status_code)
        )
        super().__init__(self.message)


class TooManyRequests(APIException):
    def __init__(self):
        super().__init__(
            status_code=429,
            message="Too many requests.",
        )


class EntityNotFound(APIException):
    def __init__(self):
        super().__init__(status_code=404, message="Entity not found.")
