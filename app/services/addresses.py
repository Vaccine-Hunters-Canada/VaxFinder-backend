from typing import List, Union

from app.schemas.addresses import AddressResponse
from app.services.base import BaseService


class AddressService(
    BaseService[AddressResponse, AddressResponse, AddressResponse]
):
    table = "address"
    db_response_schema = AddressResponse
    
