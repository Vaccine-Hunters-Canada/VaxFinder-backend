from datetime import datetime

from pydantic import BaseModel


class RequirementResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
