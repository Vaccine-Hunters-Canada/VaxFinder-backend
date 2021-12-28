from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.core.config import settings
from app.db.database import MSSQLConnection
from app.schemas.webPush import KeyResponse, SubscriptionCreateRequest
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.webPush import WebPushService

router = APIRouter()


@router.get(
    "/publicKey",
    response_model=KeyResponse,
)
async def retrieve_publicKey2() -> KeyResponse:
    """
    **Retrieves the public key**
    """
    return KeyResponse(key=settings.VAPID_Public_Key)


@router.get(
    "/public-key",
    response_model=KeyResponse,
)
async def retrieve_publicKey() -> KeyResponse:
    """
    **Retrieves the public key**
    """
    return KeyResponse(key=settings.VAPID_Public_Key)


@router.post(
    "/subscription",
    responses={
        status.HTTP_201_CREATED: {"description": "Push notification created"},
    },
)
async def create_subscription(
    body: SubscriptionCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> Response:
    """
    **Subscribes the user to push notifications for their postal code.
    """
    try:
        await WebPushService(db).CreateWebhook(body)

    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/subscription/{endpoint}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The endpoint has been deleted"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The endpoint could not " "be found."
        },
    },
)
async def delete_subscription_by_endpoint(
    endpoint: str, db: MSSQLConnection = Depends(get_db)
) -> Response:
    """
    **Deletes a subscrtiption with supplied endpoint
    parameter.**
    """

    # Perform deletion
    try:
        ret: int
        ret = await WebPushService(db).DeleteWebhook(endpoint)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if ret == 0:
    #    return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
