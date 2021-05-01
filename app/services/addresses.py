from typing import Type

from app.schemas.addresses import (
    AddressResponse,
    AddressCreateRequest,
    AddressUpdateRequest
)
from app.services.base import BaseService


class AddressService(
    BaseService[AddressResponse, AddressCreateRequest, AddressUpdateRequest]
):
    read_procedure_id_parameter = "addressID"
    
    @property
    def table(self) -> str:
        return 'address'

    @property
    def db_response_schema(self) -> Type[AddressResponse]:
        return AddressResponse

    @property
    def create_response_schema(self) -> Type[AddressCreateRequest]:
        return AddressCreateRequest

    @property
    def update_response_schema(self) -> Type[AddressUpdateRequest]:
        return AddressUpdateRequest
