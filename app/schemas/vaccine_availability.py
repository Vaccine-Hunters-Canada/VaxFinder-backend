from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums import InputTypeEnum
from app.schemas.locations import LocationExpandedResponse
from app.schemas.misc import FilterParamsBase


class VaccineAvailabilityFilterParams(FilterParamsBase):
    postalCode: str


class VaccineAvailabilityResponseBase(BaseModel):
    numberAvaliable: int
    numberTotal: Optional[int]
    date: date
    vaccine: Optional[int]
    inputType: InputTypeEnum
    tags: Optional[str]


class VaccineAvailabilityResponse(VaccineAvailabilityResponseBase):
    id: UUID
    location: int
    created_at: datetime


class VaccineAvailabilityExpandedResponse(VaccineAvailabilityResponseBase):
    id: UUID
    location: LocationExpandedResponse
    created_at: datetime

class VaccineAvailabilityCreateRequest(VaccineAvailabilityResponseBase):
    location: int
    auth: str

class VaccineAvailabilityUpdateRequest(VaccineAvailabilityResponseBase):
    id: UUID
    location: int
    auth: str

