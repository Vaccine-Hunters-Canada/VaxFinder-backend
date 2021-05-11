from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.api_v1.pagination import AbstractPage, Page, paginate
from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.organizations import OrganizationService

router = APIRouter()


@router.get("", response_model=Page[OrganizationResponse])
async def list_organizations(
    db: MSSQLConnection = Depends(get_db),
) -> AbstractPage[OrganizationResponse]:
    """
    **Retrieves the list of organizations.**
    """
    # TODO: Filter by name
    return paginate(await OrganizationService(db).get_multi())


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The organization with the specified id could not "
            "be found."
        }
    },
)
async def retrieve_organization_by_id(
    organization_id: int, db: MSSQLConnection = Depends(get_db)
) -> OrganizationResponse:
    """
    **Retrieves an organization with the id from the `organization_id` path
    parameter.**
    """
    organization = await OrganizationService(db).get(organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization


@router.post(
    "",
    response_model=OrganizationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_organization(
    body: OrganizationCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> OrganizationResponse:
    """
    **Creates a new organization with the entity enclosed in the request
    body.** On success, the new organization is returned in the body of the
    response.
    """
    try:
        organization = await OrganizationService(db).create(body, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return organization


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The organization with the specified id could not "
            "be found."
        },
    },
)
async def update_organization(
    organization_id: int,
    body: OrganizationUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> OrganizationResponse:
    """
    **Updates an organization with the id from the `organization_id` path
    parameter with the entity enclosed in the request body.** On success,
    the updated organization is returned in the body of the response.
    """
    # Check if organization with the id exists
    organization = await OrganizationService(db).get(organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform update
    try:
        organization = await OrganizationService(db).update(
            organization_id, body, api_key
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return organization


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The organization with the specified id has been "
            "successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The organization with the specified id could not "
            "be found."
        },
    },
)
async def delete_organization_by_id(
    organization_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    **Deletes an organization with the id from the `organization_id` path
    parameter.**
    """
    # Check if organization with the id exists
    organization = await OrganizationService(db).get(organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    try:
        await OrganizationService(db).delete(organization_id, api_key)
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
