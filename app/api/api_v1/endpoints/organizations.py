from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.misc import GeneralResponse
from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationFilterParams,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from app.services.organizations import OrganizationService

router = APIRouter()


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
    name: str = "", db: MSSQLConnection = Depends(get_db)
) -> List[OrganizationResponse]:
    return await OrganizationService(db).get_all(
        filters=OrganizationFilterParams(name=name, match_type="exact")
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        }
    },
)
async def retrieve_organization_by_id(
    organization_id: int, db: MSSQLConnection = Depends(get_db)
) -> OrganizationResponse:
    organization = await OrganizationService(db).get_by_id(organization_id)

    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization


@router.post(
    "",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."}
    },
)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    organization = await OrganizationService(db).create(body, api_key)

    if organization == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{organization_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        },
    },
)
async def update_organization(
    organization_id: int,
    body: OrganizationUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    organization = await OrganizationService(db).update(
        identifier=organization_id, params=body, auth_key=api_key
    )

    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if organization == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The organization with the specified id has been "
            "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The organization with the specified id could not "
            "be found."
        },
    },
)
async def delete_organization_by_id(
    organization_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    Deletes an organization with the id from the `organization_id` path
    parameter.
    """
    # Check if organization with the id exists
    organization = await OrganizationService(db).get_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    deleted = await OrganizationService(db).delete_by_id(
        organization_id, api_key
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
