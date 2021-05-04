from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    full_name: Optional[str]
    short_name: str
    description: Optional[str]
    url: Optional[str]


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime


class OrganizationCreateRequest(OrganizationBase):
    pass


class OrganizationUpdateRequest(OrganizationBase):
    # organizationID: int
    pass
