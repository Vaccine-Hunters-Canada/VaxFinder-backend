from datetime import date, datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums import InputTypeEnum
from app.schemas.locations import LocationExpandedResponse
from app.schemas.misc import FilterParamsBase


class VaccineAvailabilityFilterParams(FilterParamsBase):
    postalCode: str


class VaccineAvailabilityResponseBase(BaseModel):
    numberAvaliable: Optional[int]
    numberTotal: Optional[int]
    date: Optional[date]
    vaccine: Optional[int]
    inputType: Optional[InputTypeEnum]
    tags: Optional[str]


class VaccineAvailabilityResponse(VaccineAvailabilityResponseBase):
    id: Union[UUID, int]
    location: int
    created_at: datetime


class VaccineAvailabilityExpandedResponse(VaccineAvailabilityResponseBase):
    id: Union[UUID, int]
    location: LocationExpandedResponse
    created_at: datetime

class VaccineAvailabilityCreateRequest(VaccineAvailabilityResponseBase):
    location: int
    auth: str

class VaccineAvailabilityUpdateRequest(VaccineAvailabilityResponseBase):
    id: Union[UUID, int]
    location: int
    auth: str

