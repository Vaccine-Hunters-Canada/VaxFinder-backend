import time
import traceback
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.entries import EntryExpandedResponse
from app.services.entries import EntryService

router = APIRouter()


@router.get("", response_model=List[EntryExpandedResponse])
async def get_entries(
    postalCode: str = "", db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await EntryService(db).get_entries(postal_code=postalCode)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{entry_id}", response_model=EntryExpandedResponse)
async def get_entry(entry_id: int, db: MSSQLConnection = Depends(get_db)):
    try:
        ret = await EntryService(db).get_entry_by_id(entry_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
