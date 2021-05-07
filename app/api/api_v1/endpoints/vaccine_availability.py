from datetime import date, datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    status,
)
from loguru import logger

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityRequirementCreateRequest,
    VaccineAvailabilityRequirementCreateSprocParams,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityRequirementUpdateRequest,
    VaccineAvailabilityResponse,
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotCreateSprocParams,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotUpdateRequest,
    VaccineAvailabilityUpdateRequest,
)
from app.services.exceptions import (
    DatabaseNotInSyncError,
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)
from app.services.vaccine_availability import VaccineAvailabilityService
from app.services.vaccine_availability_requirement import (
    VaccineAvailabilityRequirementService,
)
from app.services.vaccine_availability_timeslot import (
    VaccineAvailabilityTimeslotService,
)

router = APIRouter()


@router.get("", response_model=List[VaccineAvailabilityExpandedResponse])
async def list_vaccine_availability(
    min_date: Optional[date] = Query(
        date.today(),
        title="Minimum Date",
        description="**Search for vaccine availabilities after a certain date "
        "and time (UTC) in the format YYYY-MM-DD**. The default value is the current date ("
        "UTC).<br/><br/>Valid example(s): *2021-05-30*",
    ),
    postal_code: str = Query(
        ...,
        title="Postal Code",
        description="**Search for vaccine availabilities within the vicinity "
        "of a postal code. (First 3 characters ONLY)**"
        "<br/><br/>Valid example(s): *K1A; M5V;* ",
        min_length=3,
        max_length=3,
    ),
    db: MSSQLConnection = Depends(get_db),
) -> List[VaccineAvailabilityExpandedResponse]:
    """
    **Retrieves the list of vaccine availabilities within the vicinity of a
    `postal_code` and after the `min_date`.**
    """
    # Done here so the OpenAPI spec doesn't show the wrong default value
    if min_date is None:
        min_date = datetime.today()
        min_date = min_date.replace(tzinfo=timezone.utc)
    try:
        availabilities = await VaccineAvailabilityService(
            db
        ).get_filtered_multi_expanded(
            postal_code=postal_code,
            min_date=min_date,
        )
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    except DatabaseNotInSyncError as e:
        logger.warning("Database not in sync: {}", e.message)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return availabilities


@router.get(
    "/{vaccine_availability_id}",
    response_model=VaccineAvailabilityExpandedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        }
    },
)
async def retrieve_vaccine_availability_by_id(
    vaccine_availability_id: UUID,
    db: MSSQLConnection = Depends(get_db),
) -> VaccineAvailabilityExpandedResponse:
    """
    **Retrieves a vaccine availability with the id from the
    `vaccine_availability_id` path parameter.**
    """
    entry = await VaccineAvailabilityService(db).get_expanded(
        vaccine_availability_id
    )
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry


@router.post(
    "",
    response_model=VaccineAvailabilityResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_vaccine_availability(
    body: VaccineAvailabilityCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> VaccineAvailabilityResponse:
    """
    **Creates a new vaccine availability with the entity enclosed in the
    request body.** On success, the new vaccine availability is returned in the
    body of the response.
    """
    try:
        availability = await VaccineAvailabilityService(db).create(
            body, api_key
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return availability


@router.put(
    "/{vaccine_availability_id}",
    response_model=VaccineAvailabilityResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        },
    },
)
async def update_vaccine_availability(
    vaccine_availability_id: UUID,
    body: VaccineAvailabilityUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> VaccineAvailabilityResponse:
    """
    **Updates a vaccine availability with the id from the
    `vaccine_availability_id` path parameter with the entity enclosed in the
    request body.** On success, the updated vaccine availability is returned in
    the body of the response.
    """
    # Check if vaccine availability with the id exists
    availability = await VaccineAvailabilityService(db).get(
        vaccine_availability_id
    )
    if not availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform update
    try:
        availability = await VaccineAvailabilityService(db).update(
            identifier=vaccine_availability_id, params=body, auth_key=api_key
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return availability


@router.delete(
    "/{vaccine_availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The vaccine availability with the specified id "
            "has been successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        },
    },
)
async def delete_vaccine_availability_by_id(
    vaccine_availability_id: UUID,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    **Deletes a vaccine availability with the id from the
    `vaccine_availability_id` path parameter.**
    """
    # Check if vaccine availability with the id exists
    availability = await VaccineAvailabilityService(db).get(
        vaccine_availability_id
    )
    if not availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    try:
        await VaccineAvailabilityService(db).delete(
            vaccine_availability_id, api_key
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ------------------------- Timeslots -------------------------
@router.get(
    "/{vaccine_availability_id}/timeslots",
    response_model=List[VaccineAvailabilityTimeslotResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        }
    },
)
async def list_timeslots_for_vaccine_availability_by_id(
    vaccine_availability_id: UUID = Path(
        ...,
        description="Timeslots for a vaccine availability with this id.",
    ),
    db: MSSQLConnection = Depends(get_db),
) -> List[VaccineAvailabilityTimeslotResponse]:
    """
    **Retrieves the list of timeslots for a vaccine availability. This
    vaccine availability has an ID of `vaccine_availability_id` from the
    path.**
    """
    # TODO: Filter by vaccine availability
    timeslots = await VaccineAvailabilityTimeslotService(
        db
    ).get_by_vaccine_availability_id(vaccine_availability_id)
    if timeslots is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return timeslots


@router.post(
    "/{vaccine_availability_id}/timeslots",
    response_model=VaccineAvailabilityTimeslotResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_timeslot_for_vaccine_availability_by_id(
    body: VaccineAvailabilityTimeslotCreateRequest,
    vaccine_availability_id: UUID = Path(
        ...,
        description="Timeslot for a vaccine availability with this id.",
    ),
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> VaccineAvailabilityTimeslotResponse:
    """
    **Creates a new timeslot for a vaccine availability with the entity
    enclosed in the request body. This vaccine availability has an ID of
    `vaccine_availability_id` from the path.** On success, the new timeslot is
    returned in the body of the response.
    """
    try:
        timeslot = await VaccineAvailabilityTimeslotService(db).create(
            params=VaccineAvailabilityTimeslotCreateSprocParams(
                parentID=vaccine_availability_id, time=body.time
            ),
            auth_key=api_key,
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return timeslot


# @router.put(
#     "/{vaccine_availability_id}/timeslots/{timeslot_id}",
#     response_model=VaccineAvailabilityTimeslotResponse,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
#         status.HTTP_403_FORBIDDEN: {
#             "description": "Invalid permissions or credentials."
#         },
#         status.HTTP_404_NOT_FOUND: {
#             "description": "The vaccine availability with the id from the "
#             "`vaccine_availability_id` path parameter or "
#             "the timeslot with the id from the `timeslot_id` "
#             "path parameter could not be found."
#         },
#     },
# )
# async def update_timeslot_for_vaccine_availability_by_id(
#     timeslot_id: UUID,
#     body: VaccineAvailabilityTimeslotUpdateRequest,
#     vaccine_availability_id: UUID = Path(
#         ...,
#         description="Timeslot for a vaccine availability with this id.",
#     ),
#     db: MSSQLConnection = Depends(get_db),
#     api_key: UUID = Depends(get_api_key),
# ) -> VaccineAvailabilityTimeslotResponse:
#     """
#     **Updates a timeslot with the id from the `timeslot_id` path parameter
#     with the entity enclosed in the request body. The timeslot must be
#     for a vaccine availability that has an ID of `vaccine_availability_id`
#     from the path.** On success, the updated timeslot is returned in the body
#     of the response.
#     """
#     # TODO: Check vaccine_availability_id against body
#     # Check if timeslot with the id exists
#     timeslot = await VaccineAvailabilityTimeslotService(db).get(timeslot_id)
#     if not timeslot:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     # Perform update
#     try:
#         timeslot = await VaccineAvailabilityTimeslotService(db).update(
#             timeslot_id, body, api_key
#         )
#     except InvalidAuthenticationKeyForRequest as e:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
#     except InternalDatabaseError:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return timeslot


# ------------------------- Requirements -------------------------
# @router.get(
#     "/{vaccine_availability_id}/requirements",
#     response_model=List[VaccineAvailabilityRequirementsResponse],
#     responses={
#         status.HTTP_404_NOT_FOUND: {
#             "description": "The vaccine availability with the specified id "
#             "could not be found."
#         }
#     },
# )
# async def list_requirements_for_vaccine_availability_by_id(
#     vaccine_availability_id: UUID = Path(
#         ...,
#         description="Requirements for a vaccine availability with this id.",
#     ),
#     db: MSSQLConnection = Depends(get_db),
# ) -> List[VaccineAvailabilityRequirementsResponse]:
#     """
#     **Retrieves the list of requirements for a vaccine availability. This
#     vaccine availability has an ID of `vaccine_availability_id` from the
#     path.**
#     """
#     # TODO: Filter by vaccine availability
#     requirements = await VaccineAvailabilityRequirementService(db).get_multi()
#     if requirements is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return requirements


@router.post(
    "/{vaccine_availability_id}/requirements",
    response_model=VaccineAvailabilityRequirementsResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_403_FORBIDDEN: {
            "description": "Invalid permissions or credentials."
        },
    },
)
async def create_requirement_for_vaccine_availability_by_id(
    body: VaccineAvailabilityRequirementCreateRequest,
    vaccine_availability_id: UUID = Path(
        ...,
        description="Requirement for a vaccine availability with this id.",
    ),
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> VaccineAvailabilityRequirementsResponse:
    """
    **Creates a new requirements for a vaccine availability with the entity
    enclosed in the request body. This vaccine availability has an ID of
    `vaccine_availability_id` from the path.** On success, the new timeslot is
    returned in the body of the response.
    """
    try:
        requirement = await VaccineAvailabilityRequirementService(db).create(
            params=VaccineAvailabilityRequirementCreateSprocParams(
                vaccine_availability=vaccine_availability_id,
                requirement=body.requirement,
            ),
            auth_key=api_key,
        )
    except InvalidAuthenticationKeyForRequest as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
    except InternalDatabaseError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return requirement


# @router.put(
#     "/{vaccine_availability_id}/requirements/{requirement_id}",
#     response_model=VaccineAvailabilityRequirementsResponse,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
#         status.HTTP_403_FORBIDDEN: {
#             "description": "Invalid permissions or credentials."
#         },
#         status.HTTP_404_NOT_FOUND: {
#             "description": "The vaccine availability with the id from the "
#             "`vaccine_availability_id` path parameter or "
#             "the requirement with the id from the "
#             "`requirement_id` path parameter could not be "
#             "found."
#         },
#     },
# )
# async def update_requirement_for_vaccine_availability_by_id(
#     requirement_id: UUID,
#     body: VaccineAvailabilityRequirementUpdateRequest,
#     vaccine_availability_id: UUID = Path(
#         ...,
#         description="Requirement for a vaccine availability with this id.",
#     ),
#     db: MSSQLConnection = Depends(get_db),
#     api_key: UUID = Depends(get_api_key),
# ) -> VaccineAvailabilityRequirementsResponse:
#     """
#     **Updates a requirement with the id from the `requirement_id` path
#     parameter with the entity enclosed in the request body. The requirement
#     must be for a vaccine availability that has an ID of
#     `vaccine_availability_id` from the path.** On success, the updated
#     requirement is returned in the body of the response.
#     """
#     # TODO: Check vaccine_availability_id against body
#     # Check if vaccine availability requirement with the id exists
#     requirement = await VaccineAvailabilityRequirementService(db).get(
#         requirement_id
#     )
#     if not requirement:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     # Perform update
#     try:
#         requirement = await VaccineAvailabilityRequirementService(db).update(
#             requirement_id, body, api_key
#         )
#     except InvalidAuthenticationKeyForRequest as e:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, e.message)
#     except InternalDatabaseError:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return requirement
