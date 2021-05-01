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
async def list(
    postalCode: str = "",
    db: MSSQLConnection = Depends(get_db)
) -> List[EntryExpandedResponse]:
    return await EntryService(db).get_all(
        filters={"postalCode": ("exact", postalCode)}
    )


@router.get(
    "/{entry_id}",
    response_model=EntryExpandedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The entry with the specified id could not be found."
        }
    },
)
async def retrieve(
    entry_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> EntryExpandedResponse:
    entry = await EntryService(db).get_by_id(entry_id)

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry
