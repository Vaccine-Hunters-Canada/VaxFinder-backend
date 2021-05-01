from app.schemas.misc import FilterParamsBase
from datetime import datetime
from typing import Union

from pydantic import BaseModel

from app.schemas.addresses import AddressResponse

class LocationFilterParams(FilterParamsBase):
    postalCode: str
class LocationResponseBase(BaseModel):
    id: int
    name: str
    organization: str
    phone: str
    notes: str
    active: int
    postcode: str
    created_at: datetime

class LocationResponse(LocationResponseBase):
    address: int

class LocationExpandedResponse(LocationResponseBase):
    address: AddressResponse
