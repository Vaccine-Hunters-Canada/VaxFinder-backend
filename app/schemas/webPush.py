from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.schemas.base import BaseModel


class KeyResponse(BaseModel):
    key: str


class SubscriptionUpdateRequest(BaseModel):
    endpoint: str


class SubscriptionBase(BaseModel):
    endpoint: str
    auth: str
    p256dh: str
    postalCode: str


class SubscriptionResponse(SubscriptionBase):
    id: int
    created: datetime


class SubscriptionCreateRequest(SubscriptionBase):
    pass
