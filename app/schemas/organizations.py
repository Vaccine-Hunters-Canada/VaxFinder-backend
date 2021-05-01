from app.schemas.misc import FilterParamsBase
from datetime import date, datetime

from pydantic import BaseModel

class OrganizationFilterParams(FilterParamsBase):
    name: str

class OrganizationResponse(BaseModel):
    id: int
    full_name: str
    short_name: str
    description: str
    created_at: datetime


class OrganizationCreateRequest(BaseModel):
    full_name: str
    short_name: str
    description: str
