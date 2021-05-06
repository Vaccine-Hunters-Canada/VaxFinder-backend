from datetime import datetime

from app.schemas.base import BaseModel


class RequirementResponseBase(BaseModel):
    name: str
    description: str


class RequirementResponse(RequirementResponseBase):
    id: int
    created_at: datetime


class RequirementsCreateRequest(RequirementResponseBase):
    pass


class RequirementsUpdateRequest(RequirementResponseBase):
    id: int
