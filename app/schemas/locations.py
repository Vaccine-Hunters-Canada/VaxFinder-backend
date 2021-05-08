from datetime import datetime
from typing import Optional

from pydantic import HttpUrl
from pydantic.types import NonNegativeInt

from app.schemas.addresses import AddressResponse
from app.schemas.base import BaseModel
from app.schemas.organizations import OrganizationResponse


class LocationResponseBase(BaseModel):
    name: str
    phone: Optional[str]
    notes: Optional[str]
    active: int
    postcode: Optional[str]
    url: Optional[HttpUrl]
    tags: Optional[str]


class LocationResponse(LocationResponseBase):
    id: NonNegativeInt
    organization: Optional[int]
    address: Optional[int]
    created_at: datetime


class LocationExpandedResponse(LocationResponseBase):
    id: NonNegativeInt
    organization: Optional[OrganizationResponse]
    address: Optional[AddressResponse]
    created_at: datetime


class LocationCreateRequest(LocationResponseBase):
    organization: Optional[int]
    address: Optional[int]


class LocationUpdateRequest(LocationResponseBase):
    id: NonNegativeInt
    address: Optional[int]
    organization: Optional[int]
