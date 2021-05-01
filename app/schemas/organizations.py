from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.misc import FilterParamsBase


class OrganizationFilterParams(FilterParamsBase):
    name: str


class OrganizationResponse(BaseModel):
    id: int
    full_name: Optional[str]
    short_name: str
    description: Optional[str]
    url: Optional[str]
    created_at: datetime


class OrganizationCreateRequest(BaseModel):
    full_name: Optional[str]
    short_name: str
    description: Optional[str]
    url: Optional[str]
