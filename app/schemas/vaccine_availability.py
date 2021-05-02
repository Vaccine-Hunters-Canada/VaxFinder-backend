from datetime import date, datetime
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums import InputTypeEnum
from app.schemas.locations import LocationExpandedResponse
from app.schemas.misc import FilterParamsBase


class VaccineAvailabilityFilterParams(FilterParamsBase):
    postalCode: str

class VaccineAvailabilityResponseBase(BaseModel):
    numberAvailable: Optional[int]
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

# ------------------------- Timeslots -------------------------
#region 
class VaccineAvailabilityTimeslotResponse(BaseModel):
    id: UUID
    vaccine_availability: UUID
    active: bool
    taken_at: Optional[datetime]
    created_at: datetime
    time: datetime

class VaccineAvailabilityTimeslotCreateRequest(BaseModel):
    parentID: UUID
    auth: str
    time: datetime

class VaccineAvailabilityTimeslotUpdateRequest(BaseModel):
    # auth: str
    taken_at: Optional[datetime]

class VaccineAvailabilityTimeslotFilterParams(FilterParamsBase):
    vaccine_availability: UUID
#endregion

# ------------------------- Requirements -------------------------
#region

class VaccineAvailabilityRequirementsResponse(BaseModel):
    id: int
    vaccine_availability: UUID
    requirement: int
    active: bool
    created_at: datetime

class VaccineAvailabilityRequirementsCreateRequest(BaseModel):
    requirements: List[int]

class VaccineAvailabilityRequirementsUpdateRequest(BaseModel):
    active: bool

class VaccineAvailabilityRequirementsFilterParams(FilterParamsBase):
    vaccine_availability: UUID
#endregion
