from typing import List, Optional, Type
from uuid import UUID

from pywebpush import WebPushException, webpush

from app.core.config import settings
from app.schemas.webPush import (
    KeyResponse,
    SubscriptionBase,
    SubscriptionCreateRequest,
    SubscriptionResponse,
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
        return KeyResponse(key=settings.VAPID_Public_Key)

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

    async def ReadByPostal(self, postal: str) -> List[SubscriptionResponse]:
        procedure_name = "subscription_ReadByPostal"

        ret_value, db_rows = await self._db.sproc_fetch_all(
            procedure_name,
            parameters={"postal": postal},
        )

        if db_rows is None:
            # We are assuming that any error on the stored procedure is due
            # to the fact that the object doesn't exist.
            return []

        return [SubscriptionResponse(**o) for o in db_rows]

    async def SendWebpush(self, postal: str, location: Optional[int]) -> int:

        subscriptions = await self.ReadByPostal(postal)

        if len(subscriptions) > 0:
            for subscription in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.p256dh,
                                "auth": subscription.auth,
                            },
                        },
                        data='{locationId: "' + str(location) + '"}',
                        vapid_private_key=settings.VAPID_Public_Key,
                        vapid_claims={
                            "sub": "mailto:contact@vaccinehunters.ca",
                        },
                    )
                except WebPushException as ex:
                    if ex.response and ex.response.json():
                        extra = ex.response.json()
                        # Do actual logging...
                        print(
                            "Remote service replied with a {}:{}, {}",
                            extra.code,
                            extra.errno,
                            extra.message,
                        )

        return 1
