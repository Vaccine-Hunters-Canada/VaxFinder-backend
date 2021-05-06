from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.requirements import (
    RequirementResponse,
    RequirementsCreateRequest,
    RequirementsUpdateRequest,
)
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.requirements import RequirementService

router = APIRouter()


@router.get("", response_model=List[RequirementResponse])
async def list_requirements(
    db: MSSQLConnection = Depends(get_db),
) -> List[RequirementResponse]:
    """
    **Retrieves the list of requirements.**
    """
    return await RequirementService(db).get_multi()


@router.get(
    "/{requirement_id}",
    response_model=RequirementResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The requirement with the specified id could not "
            "be found."
        }
    },
)
async def retrieve_requirement_by_id(
    requirement_id: int, db: MSSQLConnection = Depends(get_db)
) -> RequirementResponse:
    """
    **Retrieves a requirement with the id from the `requirement_id` path
    parameter.**
    """
    requirement = await RequirementService(db).get(requirement_id)
    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return requirement


@router.post(
    "",
    response_model=RequirementResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_requirement(
    body: RequirementsCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> RequirementResponse:
    """
    **Creates a new requirement with the entity enclosed in the request
    body.** On success, the new requirement is returned in the body of the
    response.
    """
    try:
        requirement = await RequirementService(db).create(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return requirement


@router.put(
    "/{requirement_id}",
    response_model=RequirementResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        },
    },
)
async def update_requirement(
    requirement_id: int,
    body: RequirementsUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> RequirementResponse:
    """
    **Updates a requirement with the id from the `requirement_id` path
    parameter with the entity enclosed in the request body.** On success,
    the updated requirement is returned in the body of the response.
    """
    # Check if requirement with the id exists
    requirement = await RequirementService(db).get(requirement_id)
    if not requirement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform update
    try:
        requirement = await RequirementService(db).update(
            requirement_id, body, api_key
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return requirement


@router.delete(
    "/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The requirement with the specified id has been "
            "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The requirement with the specified id could not "
            "be found."
        },
    },
)
async def delete_requirement_by_id(
    requirement_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    **Deletes a requirement with the id from the `requirement_id` path
    parameter.**
    """
    # Check if requirement with the id exists
    requirement = await RequirementService(db).get(requirement_id)
    if not requirement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    try:
        await RequirementService(db).delete(requirement_id, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
