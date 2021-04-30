from datetime import date, datetime
from typing import Union

from pydantic import BaseModel

from app.schemas.locations import LocationExpandedResponse


class EntryResponse(BaseModel):
    id: int
    numberAvaliable: int
    numberTotal: int
    date: date
    location: int
    vaccine: int
    inputType: int
    tags_optional: str
    tags_required: str
    created_at: datetime


class EntryExpandedResponse(EntryResponse):
    location: LocationExpandedResponse
