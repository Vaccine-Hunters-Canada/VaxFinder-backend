from typing import Type
from uuid import UUID

from app.core.config import settings
from app.schemas.webPush import (
    KeyResponse,
    SubscriptionBase,
    SubscriptionCreateRequest,
    SubscriptionUpdateRequest,
)
from app.services.base import BaseService


class WebPushService(
    BaseService[
        SubscriptionBase, SubscriptionCreateRequest, SubscriptionUpdateRequest
    ]
):
    read_procedure_name = "subscription_Read"
    read_procedure_id_parameter = "endpoint"
    create_procedure_name = "subscription_Create"
    delete_procedure_name = "subscription_Delete"
    delete_procedure_id_parameter = "endpoint"

    @property
    def table(self) -> str:
        return "Subscription"

    @property
    def db_response_schema(self) -> Type[SubscriptionBase]:
        return SubscriptionBase

    @property
    def create_response_schema(self) -> Type[SubscriptionCreateRequest]:
        return SubscriptionCreateRequest

    @property
    def update_response_schema(self) -> Type[SubscriptionUpdateRequest]:
        return SubscriptionUpdateRequest

    async def GetKey(self) -> KeyResponse:
        return KeyResponse(key=settings.VAPID_Key)

    async def CreateWebhook(self, request: SubscriptionCreateRequest) -> None:
        procedure_name = "subscription_Create"

        ret_val = await self._db.execute_sproc(
            procedure_name,
            parameters={
                "endpoint": request.endpoint,
                "clientAuth": request.auth,
                "p256dh": request.p256dh,
                "postalCode": request.postalCode,
            },
        )

    async def DeleteWebhook(self, endpoint: str) -> int:
        procedure_name = "subscription_Delete"

        ret_val = await self._db.execute_sproc(
            procedure_name,
            parameters={"endpoint": endpoint},
        )

        if ret_val == 1:
            return 1

        return 0
