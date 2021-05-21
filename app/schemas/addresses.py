from datetime import datetime
from typing import Optional

from pydantic import ConstrainedStr

from app.schemas.base import BaseModel


class PostalCode(ConstrainedStr):
    min_length = 6
    max_length = 6


class AddressResponseBase(BaseModel):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    # TODO: Should be enum but database is string now
    province: str
    postcode: PostalCode

class AddressResponse(AddressResponseBase):
    id: int
    created_at: datetime

class AddressCreateRequest(AddressResponseBase):
    latitude: Optional[float]
    longitude: Optional[float]


class AddressUpdateRequest(AddressResponseBase):
    id: int
    latitude: Optional[float]
    longitude: Optional[float]
