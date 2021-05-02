from app.schemas.misc import GeneralResponse
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.locations import LocationCreateRequest, LocationExpandedResponse, LocationFilterParams, LocationUpdateRequest
from app.services.locations import LocationService

router = APIRouter()


@router.get("", response_model=List[LocationExpandedResponse])
async def list_locations(
    postalCode: str = "",
    db: MSSQLConnection = Depends(get_db)
) -> List[LocationExpandedResponse]:
    return await LocationService(db).get_all_expanded(
        filters=LocationFilterParams(postalCode=postalCode, match_type='exact')
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
    location_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> LocationExpandedResponse:
    location = await LocationService(db).get_by_id_expanded(location_id)

    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return location

@router.post("", response_model=GeneralResponse)
async def create_location(
    body: LocationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> GeneralResponse:
    await LocationService(db).create(body)

    return GeneralResponse(success=True)

@router.put(
    "/{location_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def update_location(
    location_id: int,
    body: LocationUpdateRequest,
    db: MSSQLConnection = Depends(get_db)
) -> GeneralResponse:
    requirement = await LocationService(db).update(
        id=location_id,
        params=body)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GeneralResponse(success=True)
