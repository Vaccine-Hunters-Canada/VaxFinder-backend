from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.base import BaseModel


class AddressResponseBase(BaseModel):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    # TODO: Should be enum but database is string now
    province: str
    postcode: str = Field(min_length=6, max_length=6)


class AddressResponse(AddressResponseBase):
    id: int
    created_at: datetime


class AddressCreateRequest(AddressResponseBase):
    latitude: float
    longitude: float


class AddressUpdateRequest(AddressResponseBase):
    id: int
    latitude: float
    longitude: float
