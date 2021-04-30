import traceback
from datetime import datetime
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

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
async def list(name: str = "", db: MSSQLConnection = Depends(get_db)):
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
async def retrieve(
    organization_id: int, db: MSSQLConnection = Depends(get_db)
):
    organization = await OrganizationService(db).get_by_id(organization_id)

    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization


@router.post("", response_model=General_Response)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
):
    await OrganizationService(db).create(
        full_name=body.full_name,
        short_name=body.short_name,
        description=body.description,
    )

    return {"success": True}
