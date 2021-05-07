from datetime import date, datetime, timezone
from typing import List, Optional, Union
from uuid import UUID

from loguru import logger
from pydantic import NonNegativeInt, validator

from app.schemas.base import BaseModel
from app.schemas.enums import InputTypeEnum
from app.schemas.locations import LocationExpandedResponse


# ------------------------- Timeslots -------------------------
class VaccineAvailabilityTimeslotResponse(BaseModel):
    id: UUID
    vaccine_availability: UUID
    active: bool
    taken_at: Optional[datetime]
    created_at: datetime
    time: datetime

    @validator("time", pre=True)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        dt = dt.replace(tzinfo=timezone.utc)
        return dt


class VaccineAvailabilityTimeslotCreateRequest(BaseModel):
    time: datetime

    @validator("time", pre=True)
    def _validate_time(cls, dt: str) -> datetime:
        if isinstance(dt, str):
            dt = dt.replace("Z", "+00:00")
            iso = datetime.fromisoformat(dt)
            if iso.tzinfo is None:
                raise ValueError(
                    """
                    ISO datestring must have timezone info.
                    i.e. 2020-12-13T21:20:37+04:00
                    """
                )
            iso = iso.astimezone(timezone.utc)
            return iso
        raise ValueError("Must input a string.")


class VaccineAvailabilityTimeslotCreateSprocParams(BaseModel):
    time: datetime
    parentID: UUID


class VaccineAvailabilityTimeslotUpdateRequest(BaseModel):
    taken_at: Optional[datetime]


# ------------------------- Requirements -------------------------


class VaccineAvailabilityRequirementsResponse(BaseModel):
    id: int
    vaccine_availability: UUID
    requirement: int
    active: bool
    created_at: datetime


class VaccineAvailabilityRequirementCreateRequest(BaseModel):
    requirement: NonNegativeInt


class VaccineAvailabilityRequirementCreateSprocParams(BaseModel):
    vaccine_availability: UUID
    requirement: NonNegativeInt


class VaccineAvailabilityRequirementUpdateSprocParams(BaseModel):
    time: datetime
    parentID: UUID


class VaccineAvailabilityRequirementUpdateRequest(BaseModel):
    active: bool


# ----------------------------- Root -----------------------------
class VaccineAvailabilityResponseBase(BaseModel):
    numberAvailable: NonNegativeInt
    numberTotal: Optional[NonNegativeInt]
    vaccine: Optional[NonNegativeInt]
    inputType: InputTypeEnum
    tags: Optional[str]


class VaccineAvailabilityResponse(VaccineAvailabilityResponseBase):
    id: UUID
    location: NonNegativeInt
    created_at: datetime
    date: datetime

    @validator("date", pre=True)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        dt = dt.replace(tzinfo=timezone.utc)
        return dt


class VaccineAvailabilityExpandedResponse(VaccineAvailabilityResponseBase):
    id: UUID
    location: LocationExpandedResponse
    created_at: datetime
    timeslots: List[VaccineAvailabilityTimeslotResponse]
    date: datetime

    @validator("date", pre=True)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        dt = dt.replace(tzinfo=timezone.utc)
        return dt


class VaccineAvailabilityCreateRequest(VaccineAvailabilityResponseBase):
    location: NonNegativeInt
    date: datetime

    @validator("date", pre=True)
    def _validate_time(cls, dt: str) -> datetime:
        if isinstance(dt, str):
            dt = dt.replace("Z", "+00:00")
            iso = datetime.fromisoformat(dt)
            if iso.tzinfo is None:
                raise ValueError(
                    """
                    ISO datestring must have timezone info.
                    i.e. 2020-12-13T21:20:37+04:00
                    """
                )
            iso = iso.astimezone(timezone.utc)
            return iso
        raise ValueError("Must input a string.")


class VaccineAvailabilityUpdateSprocParams(VaccineAvailabilityResponseBase):
    id: UUID
    location: NonNegativeInt


class VaccineAvailabilityUpdateRequest(VaccineAvailabilityResponseBase):
    location: NonNegativeInt
