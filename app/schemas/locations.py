from app.schemas.organizations import OrganizationResponse
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.addresses import AddressResponse
from app.schemas.misc import FilterParamsBase


class LocationFilterParams(FilterParamsBase):
    postalCode: str


class LocationResponseBase(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    notes: Optional[str]
    active: int
    postcode: Optional[str]
    url: Optional[str]
    tags: Optional[str]
    created_at: datetime


class LocationResponse(LocationResponseBase):
    organization: Optional[int]
    address: Optional[int]


class LocationExpandedResponse(LocationResponseBase):
    organization: Optional[OrganizationResponse]
    address: Optional[AddressResponse]

class LocationCreateRequest(LocationResponseBase):
    auth: str

class LocationUpdateRequest(LocationResponseBase):
    id: int
    auth: str
