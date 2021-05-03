from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.api.dependencies import get_db, get_api_key
from app.db.database import MSSQLConnection
from app.schemas.addresses import AddressCreateRequest, AddressResponse, \
    AddressFilterParams, AddressUpdateRequest
from app.schemas.misc import GeneralResponse
from app.services.addresses import AddressService
from uuid import UUID

router = APIRouter()


@router.get("", response_model=List[AddressResponse])
async def list_addresses(
    postalCode: str = "",
    db: MSSQLConnection = Depends(get_db)
) -> List[AddressResponse]:
    return await AddressService(db).get_all(
        filters=AddressFilterParams(postalCode=postalCode, match_type='exact')
    )


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
    address_id: int,
    db: MSSQLConnection = Depends(get_db)
) -> AddressResponse:
    address = await AddressService(db).get_by_id(address_id)

    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return address


@router.post(
    "",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        }
    },
)
async def create_address(
    body: AddressCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    address = await AddressService(db).create(body, auth_key=api_key)
    
    if address == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{address_id}",
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
async def update_address(
    address_id: int,
    body: AddressUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> GeneralResponse:
    requirement = await AddressService(db).update(
        identifier=address_id,
        params=body,
        auth_key=api_key
    )

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if requirement == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The address with the specified id has been "
                           "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The address with the specified id could not be "
                           "found."
        }
    },
)
async def delete_address_by_id(
    address_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key)
) -> Response:
    """
    Deletes an address with the id from the `address_id` path parameter.
    """
    # Check if address with the id exists
    address = await AddressService(db).get_by_id(address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    deleted = await AddressService(db).delete_by_id(address_id, api_key)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
