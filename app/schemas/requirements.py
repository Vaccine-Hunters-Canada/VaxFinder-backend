from datetime import datetime

from pydantic import BaseModel

class RequirementResponseBase(BaseModel):
    name: str
    description: str

class RequirementResponse(RequirementResponseBase):
    id: int
    created_at: datetime

class RequirementsCreateRequest(RequirementResponseBase):
    auth: str

class RequirementsUpdateRequest(RequirementResponseBase):
    id: int
    auth: str
