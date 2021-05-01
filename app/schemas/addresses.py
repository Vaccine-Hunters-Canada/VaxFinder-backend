from app.schemas.misc import FilterParamsBase
from datetime import datetime

from pydantic import BaseModel

class AddressFilterParams(FilterParamsBase):
    postalCode: str

class AddressResponse(BaseModel):
    id: int
    line1: str
    line2: str
    city: str
    province: str
    postcode: str
    latitude: float
    longitude: float
    geohash: str
    created_at: datetime
