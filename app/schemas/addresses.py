from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.misc import FilterParamsBase


class AddressFilterParams(FilterParamsBase):
    postalCode: str


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
    pass


class AddressUpdateRequest(AddressResponseBase):
    id: int
    auth: str
