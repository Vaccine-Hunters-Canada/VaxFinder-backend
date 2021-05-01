from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.misc import General_Response
from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
)
from app.services.organizations import OrganizationService

router = APIRouter()


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
    name: str = "",
    db: MSSQLConnection = Depends(get_db)
) -> List[OrganizationResponse]:
    return await OrganizationService(db).get_all(
        filters={"name": ("exact", name)}
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


@router.post("", response_model=General_Response)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> General_Response:
    await OrganizationService(db).create(
        full_name=body.full_name,
        short_name=body.short_name,
        description=body.description,
    )

    return General_Response(success=True)
