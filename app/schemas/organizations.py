from datetime import datetime
from typing import Optional

from pydantic import HttpUrl

from app.schemas.base import BaseModel


class OrganizationBase(BaseModel):
    full_name: Optional[str]
    short_name: str
    description: Optional[str]
    url: Optional[HttpUrl]


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime


class OrganizationCreateRequest(OrganizationBase):
    pass


class OrganizationUpdateRequest(OrganizationBase):
    pass
