from typing import AsyncGenerator, Optional
from uuid import UUID

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.db.database import MSSQLConnection, db

auth_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_db() -> AsyncGenerator[MSSQLConnection, None]:
    """
    Returns a database object that will subsequently be used for making queries
    to the database for each HTTP request.
    """
    connection = db.connection

    try:
        await connection.acquire(autocommit=True)
        yield connection
    finally:
        await connection.release()


async def get_api_key(
    auth_value: Optional[str] = Security(auth_header),
) -> UUID:
    """
    Returns an API key from the Authorization header. The syntax for this
    header's value is `<type> <credentials>`. The Bearer authentication scheme
    is described by RFC6750 for OAuth 2.0 but we can still use it since the
    terminology of a Bearer token is described as:
    "A security token with the property that any party in possession of the
    token (a "bearer") can use the token in any way that any other party in
    possession of it can. Using a bearer token does not require a bearer to
    prove possession of cryptographic key material (proof-of-possession)."
    """
    auth_credentials = None
    if auth_value is not None:
        auth_values = auth_value.split()
        if len(auth_values) == 2 and auth_values[0].lower() == "bearer":
            try:
                # The authentication credentials must be a UUID
                auth_credentials = UUID(auth_values[1])
            except ValueError:
                pass

    if auth_credentials is None:
        # Give generic error for security reasons
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    return auth_credentials
