from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyUrl

from app.schemas.misc import FilterParamsBase


class OrganizationFilterParams(FilterParamsBase):
    name: str

class OrganizationBase(BaseModel):
    full_name: Optional[str]
    short_name: str
    description: Optional[str]
    url: Optional[str]

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime

class OrganizationCreateRequest(OrganizationBase):
    auth: str

class OrganizationUpdateRequest(OrganizationBase):
    # organizationID: int
    auth: str
