import time
import traceback
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel

from app.api.dependencies import get_db
from app.services.locations import LocationService
from app.db.database import MSSQLConnection
from app.schemas.locations import LocationExpandedResponse

router = APIRouter()


@router.get("", response_model=List[LocationExpandedResponse])
async def get_locations(
    postalCode: str = "", db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await LocationService(db).get_locations(
            postal_code=postalCode
        )

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{location_id}", response_model=LocationExpandedResponse)
async def get_location(
    location_id: int, db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await LocationService(db).get_location_by_id(location_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
