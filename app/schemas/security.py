from datetime import datetime

from app.schemas.base import BaseModel
from typing import List, Optional
from uuid import UUID

class SecurityResponseBase(BaseModel):
    name : str
    password : str
    

class SecurityResponse(SecurityResponseBase):
    id: int
    created_at: datetime
    key : UUID


class SecurityCreateRequest(SecurityResponseBase):
    pass


class SecurityUpdateRequest(SecurityResponseBase):
    id: int
    key : UUID


class SecurityLoginResponse(BaseModel):
    result : int
    key : Optional[UUID]
