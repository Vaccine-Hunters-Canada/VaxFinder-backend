from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.security import (
    SecurityLoginResponse,
    SecurityResponseBase,
)
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.security import SecurityService

router = APIRouter()

@router.get(
    "/login",
    response_model=SecurityLoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def login(    
    body: SecurityResponseBase,
    db: MSSQLConnection = Depends(get_db)
) -> SecurityLoginResponse:
    """
    **Creates a new vaccine availability with the entity enclosed in the
    request body.** On success, the new vaccine availability is returned in the
    body of the response.
    """
    try:
        resp: SecurityLoginResponse = (
            await SecurityService(db).Login(
                body.name,
                body.password
            )
        )

    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return resp
