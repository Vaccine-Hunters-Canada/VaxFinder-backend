from datetime import date, datetime

from pydantic import BaseModel


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
