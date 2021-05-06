from datetime import datetime
from typing import Optional

from pydantic import HttpUrl

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
    id: int
    organization: Optional[int]
    address: Optional[int]
    created_at: datetime


class LocationExpandedResponse(LocationResponseBase):
    id: int
    organization: Optional[OrganizationResponse]
    address: Optional[AddressResponse]
    created_at: datetime


class LocationCreateRequest(LocationResponseBase):
    organization: Optional[int]
    address: Optional[int]


class LocationUpdateRequest(LocationResponseBase):
    id: int
    address: Optional[int]
    organization: Optional[int]
