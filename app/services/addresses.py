from typing import Type

from app.schemas.addresses import AddressResponse
from app.services.base import BaseService


class AddressService(
    BaseService[AddressResponse, AddressResponse, AddressResponse]
):
    read_procedure_id_parameter = "addressID"
    
    @property
    def table(self) -> str:
        return 'address'

    @property
    def db_response_schema(self) -> Type[AddressResponse]:
        return AddressResponse
