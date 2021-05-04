from typing import Optional


class BaseServiceException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is not None:
            self.message = msg


class InvalidAuthenticationKeyForRequest(BaseServiceException):
    message = "Authentication key is invalid for request."


class InternalDatabaseError(BaseServiceException):
    message = "Internal server error."
