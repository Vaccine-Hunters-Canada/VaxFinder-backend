from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.api_v1.pagination import AbstractPage, Page, paginate
from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.locations import (
    LocationCreateRequest,
    LocationCreateRequestExpanded,
    LocationExpandedResponse,
    LocationResponse,
    LocationUpdateRequest,
    LocationCreateRequestExpanded
)
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.locations import LocationService

router = APIRouter()


@router.get("", response_model=Page[LocationExpandedResponse])
async def list_locations(
    db: MSSQLConnection = Depends(get_db),
) -> AbstractPage[LocationExpandedResponse]:
    """
    **Retrieves the list of locations.**
    """
    # TODO: Filter by postal code
    return paginate(await LocationService(db).get_multi_expanded())


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
    location_id: int, db: MSSQLConnection = Depends(get_db)
) -> LocationExpandedResponse:
    """
    **Retrieves a location with the id from the `location_id` path
    parameter.**
    """
    location = await LocationService(db).get_expanded(location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return location

@router.get(
    "/organization/{organization_id}",
    response_model=List[LocationExpandedResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        }
    },
)
async def retrieve_locations_by_organization(
    organization_id: int, db: MSSQLConnection = Depends(get_db)
) -> List[LocationExpandedResponse]:
    """
    **Retrieves a location with the id from the `organization_id` path
    parameter.**
    """
    locations = await LocationService(db).get_multi_expanded_org(organization_id)
    if locations is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return locations

@router.get(
    "/external/{external_key}",
    response_model=LocationExpandedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        }
    },
)
async def retrieve_location_by_external_key(
    external_key: str, db: MSSQLConnection = Depends(get_db)
) -> LocationExpandedResponse:
    """
    **Retrieves a location with the external key from the path
    parameter.**
    """
    location = await LocationService(db).get_expanded_key(external_key)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return location


@router.post(
    "",
    response_model=LocationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_location(
    body: LocationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> LocationResponse:
    """
    **Creates a new location with the entity enclosed in the request body.** On
    success, the new location is returned in the body of the response.
    """
    try:
        location = await LocationService(db).create(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return location

@router.post(
    "/expanded/",
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_location_expanded(
    body: LocationCreateRequestExpanded,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> int:
    """
    **Creates a new location with the entity enclosed in the request body.** On
    success, the new location is returned in the body of the response.
    """
    try:
        location = await LocationService(db).create_expanded(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return location

@router.post(
    "/expanded",
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_location_expanded(
    body: LocationCreateRequestExpanded,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> int:
    """
    **Creates a new location with the entity enclosed in the request body.** On
    success, the new location is returned in the body of the response.
    """
    try:
        location = await LocationService(db).create_expanded(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return location


@router.put(
    "/{location_id}",
    response_model=LocationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        },
    },
)
async def update_location(
    location_id: int,
    body: LocationUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> LocationResponse:
    """
    **Updates a location with the id from the `location_id` path parameter
    with the entity enclosed in the request body.** On success, the updated
    location is returned in the body of the response.
    """
    # Check if location with the id exists
    location = await LocationService(db).get(location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform update
    try:
        location = await LocationService(db).update(location_id, body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return location


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The location with the specified id has been "
            "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be "
            "found."
        },
    },
)
async def delete_location_by_id(
    location_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    **Deletes a location with the id from the `location_id` path parameter.**
    """
    # Check if location with the id exists
    location = await LocationService(db).get(location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    try:
        await LocationService(db).delete(location_id, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
