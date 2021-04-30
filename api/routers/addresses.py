from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List
import traceback
from datetime import datetime

from api.database.database import MSSQLConnection
from api.database import crud_service
from api.database.crud_service import Address_Read_Procedure_Response

from api.dependencies import get_db
from loguru import logger
import time

router = APIRouter()

@router.get('/', response_model=List[Address_Read_Procedure_Response])
async def get_addresses(
    postalCode: str = '',
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Addresses(db).get_addresses(postal_code=postalCode)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.get('/{address_id}', response_model=Address_Read_Procedure_Response)
async def get_address(
    address_id: int,
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Addresses(db).get_address_by_id(address_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )