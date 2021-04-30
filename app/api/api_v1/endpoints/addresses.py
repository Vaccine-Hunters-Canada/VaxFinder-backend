import time
import traceback
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel

from app.api.dependencies import get_db
from app.services.addresses import AddressService
from app.db.database import MSSQLConnection
from app.schemas.addresses import AddressResponse

router = APIRouter()


@router.get("", response_model=List[AddressResponse])
async def get_addresses(
    postalCode: str = "", db: MSSQLConnection = Depends(get_db)
):
    try:
        ret = await AddressService(db).get_addresses(
            postal_code=postalCode
        )

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(address_id: int, db: MSSQLConnection = Depends(get_db)):
    try:
        ret = await AddressService(db).get_address_by_id(address_id)

        return ret
    except Exception as e:
        logger.critical(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
