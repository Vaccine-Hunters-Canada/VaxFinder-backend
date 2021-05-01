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
    id: UUID
    numberAvaliable: int
    numberTotal: Optional[int]
    date: date
    vaccine: Optional[int]
    inputType: InputTypeEnum
    tags: Optional[str]
    created_at: datetime


class VaccineAvailabilityResponse(VaccineAvailabilityResponseBase):
    location: int


class VaccineAvailabilityExpandedResponse(VaccineAvailabilityResponseBase):
    location: LocationExpandedResponse
