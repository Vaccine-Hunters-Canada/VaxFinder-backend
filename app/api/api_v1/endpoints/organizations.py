from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
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
    name: str = "",
    db: MSSQLConnection = Depends(get_db)
) -> List[OrganizationResponse]:
    return await OrganizationService(db).get_all(
        filters=OrganizationFilterParams(name=name, match_type='exact')
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def retrieve_organization_by_id(
    organization_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> OrganizationResponse:
    organization = await OrganizationService(db).get_by_id(organization_id)

    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization


@router.post("", response_model=GeneralResponse)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> GeneralResponse:
    await OrganizationService(db).create(body)

    return GeneralResponse(success=True)

@router.put(
    "/{organization_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def update_organization(
    organization_id: int,
    body: OrganizationUpdateRequest,
    db: MSSQLConnection = Depends(get_db)
) -> OrganizationResponse:
    organization = await OrganizationService(db).update(
        id=organization_id,
        params=body)

    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization
