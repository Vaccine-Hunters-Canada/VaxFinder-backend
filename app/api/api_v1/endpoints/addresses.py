from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.addresses import (
    AddressCreateRequest,
    AddressResponse,
    AddressUpdateRequest,
)
from app.services.addresses import AddressService
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)

router = APIRouter()


@router.get("", response_model=List[AddressResponse])
async def list_addresses(
    db: MSSQLConnection = Depends(get_db),
) -> List[AddressResponse]:
    """
    **Retrieves the list of addresses.**
    """
    # TODO: Filter by postal code and requirements
    return await AddressService(db).get_multi()


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The address with the specified id could not be "
            "found."
        }
    },
)
async def retrieve_address_by_id(
    address_id: int, db: MSSQLConnection = Depends(get_db)
) -> AddressResponse:
    """
    **Retrieves an address with the id from the `address_id` path parameter.**
    """
    address = await AddressService(db).get(address_id)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return address


@router.post(
    "",
    response_model=AddressResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_address(
    body: AddressCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> AddressResponse:
    """
    **Creates a new address with the entity enclosed in the request body.** On
    success, the new address is returned in the body of the response.
    """
    try:
        address = await AddressService(db).create(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return address


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
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
async def update_address(
    address_id: int,
    body: AddressUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> AddressResponse:
    """
    **Updates an address with the id from the `address_id` path parameter with
    the entity enclosed in the request body.** On success, the updated address
    is returned in the body of the response.
    """
    # Check if address with the id exists
    address = await AddressService(db).get(address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform update
    try:
        address = await AddressService(db).update(address_id, body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The address with the specified id has been "
            "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The address with the specified id could not be "
            "found."
        },
    },
)
async def delete_address_by_id(
    address_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    **Deletes an address with the id from the `address_id` path parameter.**
    """
    # Check if address with the id exists
    address = await AddressService(db).get(address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    try:
        await AddressService(db).delete(address_id, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
