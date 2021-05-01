from app.schemas.addresses import AddressResponse
from app.services.base import BaseService


class AddressService(
    BaseService[AddressResponse, AddressResponse, AddressResponse]
):
    table = "address"
    db_response_schema = AddressResponse
    read_procedure_id_parameter = "addressID"
