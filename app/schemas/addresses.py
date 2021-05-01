from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.misc import FilterParamsBase


class AddressFilterParams(FilterParamsBase):
    postalCode: str


class AddressResponse(BaseModel):
    id: int
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    # TODO: Should be enum but database is string now
    province: str
    postcode: str
    created_at: datetime
