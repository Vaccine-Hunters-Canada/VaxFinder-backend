from datetime import datetime
from typing import Union

from pydantic import BaseModel

from app.schemas.addresses import AddressResponse


class LocationResponse(BaseModel):
    id: int
    name: str
    organization: str
    phone: str
    notes: str
    address: int
    active: int
    postcode: str
    created_at: datetime


class LocationExpandedResponse(LocationResponse):
    address: AddressResponse
