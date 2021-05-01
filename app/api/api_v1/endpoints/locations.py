from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.locations import LocationExpandedResponse
from app.services.locations import LocationService

router = APIRouter()


@router.get("", response_model=List[LocationExpandedResponse])
async def list_locations(
    postalCode: str = "", db: MSSQLConnection = Depends(get_db)
):
    return await LocationService(db).get_all(
        filters={"postalCode": ("exact", postalCode)}
    )


@router.get(
    "/{location_id}",
    response_model=LocationExpandedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def retrieve_location_by_id(
    location_id: int, db: MSSQLConnection = Depends(get_db)
):
    location = await LocationService(db).get_by_id(location_id)

    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return location
