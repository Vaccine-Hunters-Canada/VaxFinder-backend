from app.schemas.misc import FilterParamsBase
from datetime import date, datetime
from typing import Union

from pydantic import BaseModel

from app.schemas.locations import LocationExpandedResponse

class EntryFilterParams(FilterParamsBase):
    postalCode: str

class EntryResponseBase(BaseModel):
    id: int
    numberAvaliable: int
    numberTotal: int
    date: date
    vaccine: int
    inputType: int
    tags_optional: str
    tags_required: str
    created_at: datetime

class EntryResponse(EntryResponseBase):
    location: int

class EntryExpandedResponse(EntryResponseBase):
    location: LocationExpandedResponse
