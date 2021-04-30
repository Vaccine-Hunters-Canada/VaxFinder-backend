import traceback
from datetime import datetime
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
)
from app.services.organizations import OrganizationService

router = APIRouter()


@router.get("", response_model=List[OrganizationResponse])
async def get_organizations(
    name: str = "", db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await OrganizationService(db).get_organizations(name=name)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int, db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await OrganizationService(db).get_organization_by_id(organization_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("", response_model=OrganizationResponse)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
):
    try:
        ret = await OrganizationService(db).create_organization(
            full_name=body.full_name,
            short_name=body.short_name,
            description=body.description,
        )

        if ret is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # return ret
        return {
            "id": 0,
            "full_name": "",
            "short_name": "",
            "description": "",
            "created_at": datetime.now(),
        }
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
