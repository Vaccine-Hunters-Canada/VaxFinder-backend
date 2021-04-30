from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List, Union
import traceback
from datetime import datetime

from api.database.database import MSSQLConnection
from api.database import crud_service
from api.database.crud_service import (
    Organizations_Read_Procedure_Response,
    Organizations_Create_Procedure_Request
)

from api.dependencies import get_db
from loguru import logger

router = APIRouter()

@router.get('/', response_model=List[Organizations_Read_Procedure_Response])
async def get_organizations(
    name: str = '',
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Organizations(db).get_organizations(name=name)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.get('/{organization_id}', response_model=Organizations_Read_Procedure_Response)
async def get_organization(
    organization_id: int,
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Organizations(db).get_organization_by_id(organization_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post('/', response_model=Organizations_Read_Procedure_Response)
async def create_organization(
    body: Organizations_Create_Procedure_Request,
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Organizations(db).create_organization(
            full_name=body.full_name,
            short_name=body.short_name,
            description=body.description
        )

        if ret is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # return ret
        return {
            'id': 0,
            'full_name': '',
            'short_name': '',
            'description': '',
            'created_at': datetime.now()
        }
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )