from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.misc import FilterParamsBase


class AddressFilterParams(FilterParamsBase):
    postalCode: Optional[str]
    ids: List[int]

class AddressResponseBase(BaseModel):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    # TODO: Should be enum but database is string now
    province: str
    postcode: str

class AddressResponse(AddressResponseBase):
    id: int
    created_at: datetime

class AddressCreateRequest(AddressResponseBase):
    auth: str

class AddressUpdateRequest(AddressResponseBase):
    id: int
    auth: str
