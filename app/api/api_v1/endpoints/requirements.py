from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.api.dependencies import get_db, get_api_key
from app.db.database import MSSQLConnection
from app.schemas.misc import GeneralResponse
from app.schemas.requirements import RequirementResponse, \
    RequirementsCreateRequest, RequirementsUpdateRequest
from app.services.requirements import RequirementService
from uuid import UUID

router = APIRouter()


@router.get(
    "", response_model=List[RequirementResponse]
)
async def list_requirements(
    db: MSSQLConnection = Depends(get_db)
) -> List[RequirementResponse]:
    return await RequirementService(db).get_all()


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
    requirement_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> RequirementResponse:
    requirement = await RequirementService(db).get_by_id(requirement_id)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return requirement


@router.post(
    "",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        }
    },
)
async def create_requirement(
    body: RequirementsCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    requirement = await RequirementService(db).create(body, api_key)
    
    if requirement is -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{requirement_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
                           "found."
        }
    },
)
async def update_requirement(
    requirement_id: int,
    body: RequirementsUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    requirement = await RequirementService(db).update(
        identifier=requirement_id,
        params=body,
        auth_key=api_key
    )

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if requirement is -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)


@router.delete(
    "/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The requirement with the specified id has been "
                           "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The requirement with the specified id could not "
                           "be found."
        }
    },
)
async def delete_requirement_by_id(
    requirement_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> Response:
    """
    Deletes a requirement with the id from the `requirement_id` path
    parameter.
    """
    # Check if requirement with the id exists
    requirement = await RequirementService(db).get_by_id(requirement_id)
    if not requirement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    deleted = await RequirementService(db).delete_by_id(
        requirement_id,
        api_key
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
