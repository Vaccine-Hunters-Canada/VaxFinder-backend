from app.schemas.misc import GeneralResponse
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.addresses import AddressCreateRequest, AddressResponse, AddressFilterParams, AddressUpdateRequest
from app.services.addresses import AddressService

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
            "description": "The address with the specified id could not be found."
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

@router.post("", response_model=GeneralResponse)
async def create_address(
    body: AddressCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> GeneralResponse:
    await AddressService(db).create(body)

    return GeneralResponse(success=True)

@router.put(
    "/{address_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def update_address(
    address_id: int,
    body: AddressUpdateRequest,
    db: MSSQLConnection = Depends(get_db)
) -> GeneralResponse:
    requirement = await AddressService(db).update(
        id=address_id,
        params=body)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GeneralResponse(success=True)
