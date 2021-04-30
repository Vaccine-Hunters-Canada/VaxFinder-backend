from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import List
import traceback
from datetime import datetime

from api.database.database import MSSQLConnection
from api.database import crud_service
from api.database.crud_service import Entries_Response

from api.dependencies import get_db
from loguru import logger
import time

router = APIRouter()

@router.get('/', response_model=List[Entries_Response])
async def get_entries(
    postalCode: str = '',
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Entries(db).get_entries(postal_code=postalCode)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.get('/{entry_id}', response_model=Entries_Response)
async def get_entry(
    entry_id: int,
    db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await crud_service.Entries(db).get_entry_by_id(entry_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )