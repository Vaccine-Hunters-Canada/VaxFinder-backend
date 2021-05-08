from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Union
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
    time: datetime
    taken_at: Optional[datetime]
    created_at: datetime

    @validator("time", "taken_at", pre=True)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        if dt is not None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt


class VaccineAvailabilityTimeslotCreateRequest(BaseModel):
    time: datetime

    @validator("time", pre=True)
    def _validate_time(cls, dt: str) -> datetime:
        if isinstance(dt, str):
            dt = dt.replace("Z", "+00:00")
            iso = datetime.fromisoformat(dt)
        elif isinstance(dt, datetime):
            iso = dt
        else:
            raise ValueError("Must input a string or datetime.")
        if iso.tzinfo is None:
            raise ValueError(
                """
                ISO datestring must have timezone info.
                i.e. 2020-12-13T21:20:37+04:00
                """
            )
        iso = iso.astimezone(timezone.utc)
        return iso


class VaccineAvailabilityTimeslotCreateSprocParams(
    VaccineAvailabilityTimeslotCreateRequest
):
    parentID: UUID


class VaccineAvailabilityTimeslotUpdateRequest(BaseModel):
    time: datetime
    taken_at: Optional[Union[datetime, str]]

    @validator("time", pre=True)
    def _validate_time(cls, dt: str) -> datetime:
        if isinstance(dt, str):
            dt = dt.replace("Z", "+00:00")
            iso = datetime.fromisoformat(dt)
        elif isinstance(dt, datetime):
            iso = dt
        else:
            raise ValueError("Must input a string or datetime.")
        if iso.tzinfo is None:
            raise ValueError(
                "ISO datestring must have timezone info."
                "i.e. 2020-12-13T00:00:00+04:00"
            )
        iso = iso.astimezone(timezone.utc)
        return iso

    @validator("taken_at", pre=True)
    def _validate_taken_at(
        cls, taken_at: Optional[Union[datetime, str]], values: Dict[str, Any]
    ) -> Optional[datetime]:
        if taken_at is not None:
            if isinstance(taken_at, str):
                taken_at = taken_at.replace("Z", "+00:00")
                iso = datetime.fromisoformat(taken_at)
            elif isinstance(taken_at, datetime):
                iso = taken_at
            else:
                raise ValueError("Must input a string or datetime.")
            if iso.tzinfo is None:
                raise ValueError(
                    "ISO datestring must have timezone info."
                    "i.e. 2020-12-13T00:00:00+04:00"
                )
            iso = iso.astimezone(timezone.utc)
            if iso < values["time"]:
                raise ValueError(
                    "timeslot taken_at cannot be before "
                    "the time the vaccine is offered"
                )
            return iso

        return taken_at


# ------------------------- Requirements -------------------------


class VaccineAvailabilityRequirementsResponse(BaseModel):
    id: UUID
    vaccine_availability: UUID
    requirement: int
    active: bool
    created_at: datetime


class VaccineAvailabilityRequirementCreateRequest(BaseModel):
    requirement: NonNegativeInt


class VaccineAvailabilityRequirementCreateSprocParams(
    VaccineAvailabilityRequirementCreateRequest
):
    vaccine_availability: UUID
    requirement: NonNegativeInt


class VaccineAvailabilityRequirementUpdateRequest(BaseModel):
    active: bool
    requirement: NonNegativeInt


class VaccineAvailabilityRequirementUpdateSprocParams(
    VaccineAvailabilityRequirementUpdateRequest
):
    vaccine_availability_requirement_id: UUID


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
    requirements: List[VaccineAvailabilityRequirementsResponse]
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
                    "ISO datestring must have timezone info."
                    "i.e. 2020-12-13T00:00:00+04:00"
                )
            if (
                iso.hour != 0
                or iso.minute != 0
                or iso.second != 0
                or iso.microsecond != 0
            ):
                raise ValueError(
                    "ISO datestring must be midnight "
                    "at your specified timezone "
                    "i.e. 2020-12-13T00:00:00+04:00"
                )
            iso = iso.astimezone(timezone.utc)
            return iso
        raise ValueError("Must input a string.")


class VaccineAvailabilityUpdateRequest(VaccineAvailabilityResponseBase):
    location: NonNegativeInt
    date: datetime

    @validator("date", pre=True)
    def _validate_time(cls, dt: str) -> datetime:
        if isinstance(dt, str):
            dt = dt.replace("Z", "+00:00")
            iso = datetime.fromisoformat(dt)
            if iso.tzinfo is None:
                raise ValueError(
                    "ISO datestring must have timezone info. "
                    "i.e. 2020-12-13T00:00:00+04:00"
                )
            if (
                iso.hour != 0
                or iso.minute != 0
                or iso.second != 0
                or iso.microsecond != 0
            ):
                raise ValueError(
                    "ISO datestring must be midnight "
                    "at your specified timezone "
                    "(time-specific availabilities should be inside "
                    "the availability's timeslots) "
                    "i.e. 2020-12-13T00:00:00+04:00"
                )
            iso = iso.astimezone(timezone.utc)
            return iso
        raise ValueError("Must input a string.")


class VaccineAvailabilityUpdateSprocParams(VaccineAvailabilityUpdateRequest):
    id: UUID


# ---------------------- Vaccine Locations ----------------------
class VaccineAvailabilityTimeslotRequirementExpandedResponse(
    VaccineAvailabilityResponseBase
):
    id: UUID
    location: NonNegativeInt
    created_at: datetime
    date: datetime
    timeslots: List[VaccineAvailabilityTimeslotResponse]
    requirements: List[VaccineAvailabilityRequirementsResponse]

    @validator("date", pre=True)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        dt = dt.replace(tzinfo=timezone.utc)
        return dt


class VaccineLocationExpandedResponse(LocationExpandedResponse):
    vaccine_availabilities: List[
        VaccineAvailabilityTimeslotRequirementExpandedResponse
    ]
