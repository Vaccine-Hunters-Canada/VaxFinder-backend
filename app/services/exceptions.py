from typing import Optional

from loguru import logger


class BaseServiceException(Exception):
    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is not None:
            self.message = msg
            logger.critical(self.message)


class InvalidAuthenticationKeyForRequest(BaseServiceException):
    message = "Authentication key is invalid for request."


class InternalDatabaseError(BaseServiceException):
    message = "Internal server error."


class DatabaseNotInSyncError(BaseServiceException):
    message = "Database is not in sync."
