from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.api.dependencies import get_db, get_api_key
from app.db.database import MSSQLConnection
from app.schemas.locations import LocationCreateRequest, \
    LocationExpandedResponse, LocationFilterParams, LocationUpdateRequest
from app.schemas.misc import GeneralResponse
from app.services.locations import LocationService
from uuid import UUID

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
            "description": "The location with the specified id could not be "
                           "found."
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


@router.post(
    "",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        }
    },
)
async def create_location(
    body: LocationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    location = await LocationService(db).create(body, api_key)
    
    if location == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{location_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
                           "found."
        }
    },
)
async def update_location(
    location_id: int,
    body: LocationUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    location = await LocationService(db).update(
        identifier=location_id,
        params=body,
        auth_key=api_key
    )

    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if location == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The location with the specified id has been "
                           "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
                           "found."
        }
    },
)
async def delete_location_by_id(
    location_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> Response:
    """
    Deletes a location with the id from the `location_id` path parameter.
    """
    # Check if location with the id exists
    location = await LocationService(db).get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    deleted = await LocationService(db).delete_by_id(location_id, api_key)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
