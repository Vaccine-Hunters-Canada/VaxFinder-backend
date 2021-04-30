import time
import traceback
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.addresses import AddressResponse
from app.services.addresses import AddressService

router = APIRouter()


@router.get("", response_model=List[AddressResponse])
async def list(postalCode: str = "", db: MSSQLConnection = Depends(get_db)):
    return await AddressService(db).get_all(
        filters={"postalCode": ("exact", postalCode)}
    )


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The address with the specified id could not be found."
        }
    },
)
async def retrieve(address_id: int, db: MSSQLConnection = Depends(get_db)):
    address = await AddressService(db).get_by_id(address_id)

    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return address
