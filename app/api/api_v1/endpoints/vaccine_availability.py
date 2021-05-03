from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_api_key, get_db
from app.db.database import MSSQLConnection
from app.schemas.misc import GeneralResponse
from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityFilterParams,
    VaccineAvailabilityRequirementsCreateRequest,
    VaccineAvailabilityRequirementsFilterParams,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityRequirementsUpdateRequest,
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotFilterParams,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotUpdateRequest,
    VaccineAvailabilityUpdateRequest,
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
    postalCode: str = "", db: MSSQLConnection = Depends(get_db)
) -> List[VaccineAvailabilityExpandedResponse]:
    return await VaccineAvailabilityService(db).get_all_expanded(
        filters=VaccineAvailabilityFilterParams(
            postalCode=postalCode, match_type="exact"
        )
    )


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
    vaccine_availability_id: UUID, db: MSSQLConnection = Depends(get_db)
) -> VaccineAvailabilityExpandedResponse:
    entry = await VaccineAvailabilityService(db).get_by_id_expanded(
        vaccine_availability_id
    )

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry


@router.post(
    "",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."}
    },
)
async def create_vaccine_availability(
    body: VaccineAvailabilityCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    vaccine_availability = await VaccineAvailabilityService(db).create(
        body, api_key
    )

    if vaccine_availability == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{vaccine_availability_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        },
    },
)
async def update_vaccine_availability(
    vaccine_availability_id: int,
    body: VaccineAvailabilityUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    vaccine_availability = await VaccineAvailabilityService(db).update(
        identifier=vaccine_availability_id, params=body, auth_key=api_key
    )

    if vaccine_availability is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if vaccine_availability == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)


@router.delete(
    "/{vaccine_availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The vaccine availability with the specified id "
            "has been successfully deleted."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found."
        },
    },
)
async def delete_vaccine_availability_by_id(
    vaccine_availability_id: int,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> Response:
    """
    Deletes a vaccine availability with the id from the
    `vaccine_availability_id` path parameter.
    """
    # Check if vaccine availability with the id exists
    vaccine_availability = await VaccineAvailabilityService(db).get_by_id(
        vaccine_availability_id
    )
    if not vaccine_availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Perform deletion
    deleted = await VaccineAvailabilityService(db).delete_by_id(
        vaccine_availability_id, api_key
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
async def retrieve_vaccine_availability_timeslots(
    vaccine_availability_id: UUID, db: MSSQLConnection = Depends(get_db)
) -> List[VaccineAvailabilityTimeslotResponse]:
    timeslots = await VaccineAvailabilityTimeslotService(db).get_all(
        VaccineAvailabilityTimeslotFilterParams(
            vaccine_availability=vaccine_availability_id, match_type="exact"
        )
    )

    if timeslots is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return timeslots


@router.post(
    "/{vaccine_availability_id}/timeslots",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."}
    },
)
async def create_vaccine_availability_timeslot(
    vaccine_availability_id: UUID,
    body: VaccineAvailabilityTimeslotCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    timeslot = await VaccineAvailabilityTimeslotService(db).create(
        body, api_key
    )

    if timeslot == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{vaccine_availability_id}/timeslots/{timeslot_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the id from the "
            "`vaccine_availability_id` path parameter or "
            "the timeslot with the id from the `timeslot_id` "
            "path parameter could not be found."
        },
    },
)
async def update_vaccine_availability_timeslot(
    vaccine_availability_id: UUID,
    timeslot_id: UUID,
    body: VaccineAvailabilityTimeslotUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    timeslot = await VaccineAvailabilityTimeslotService(db).update(
        identifier=timeslot_id, params=body, auth_key=api_key
    )

    if timeslot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if timeslot == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)


# TODO: This can be commented out once vaccine availability timeslot has a
#  delete stored procedure
# @router.delete(
#     "/{vaccine_availability_id}/timeslots/{timeslot_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_204_NO_CONTENT: {
#             "description": "The vaccine availability timeslot with the id "
#                            "from the `timeslot_id` path parameter has been "
#                            "successfully deleted. "
#         },
#         status.HTTP_401_UNAUTHORIZED: {
#             "description": "Invalid credentials."
#         },
#         status.HTTP_404_NOT_FOUND: {
#             "description": "The vaccine availability with the id from the "
#                            "`vaccine_availability_id` path parameter or "
#                            "the timeslot with the id from the `timeslot_id` "
#                            "path parameter could not be found."
#         }
#     },
# )
# async def delete_vaccine_availability_by_id(
#     vaccine_availability_id: int,
#     timeslot_id: int,
#     db: MSSQLConnection = Depends(get_db),
#     api_key: UUID = Depends(get_api_key)
# ) -> Response:
#     """
#     Deletes a vaccine availability timeslot with the id from the `timeslot_id`
#     path parameter. This timeslot must be under a vaccine availability with the
#     id from the `vaccine_availability_id` path parameter.
#     """
#     # Check if vaccine availability with the id exists
#     vaccine_availability = await VaccineAvailabilityService(db).get_by_id(
#         vaccine_availability_id
#     )
#     if not vaccine_availability:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     # Check if timeslot with the id exists
#     timeslot = await VaccineAvailabilityTimeslotService(db).get_by_id(
#        timeslot_id
#     )
#     if not timeslot or timeslot:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     # Perform deletion
#     deleted = await VaccineAvailabilityService(db).delete_by_id(
#         timeslot_id,
#         api_key
#     )
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# ------------------------- Requirements -------------------------
@router.get(
    "/{vaccine_availability_id}/requirements",
    response_model=List[VaccineAvailabilityRequirementsResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id "
            "could not be found. "
        }
    },
)
async def retrieve_vaccine_availability_requirements(
    vaccine_availability_id: UUID, db: MSSQLConnection = Depends(get_db)
) -> List[VaccineAvailabilityRequirementsResponse]:
    requirements = await VaccineAvailabilityRequirementService(db).get_all(
        VaccineAvailabilityRequirementsFilterParams(
            vaccine_availability=vaccine_availability_id, match_type="exact"
        )
    )

    if requirements is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return requirements


@router.post(
    "/{vaccine_availability_id}/requirements",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."}
    },
)
async def create_vaccine_availability_requirement(
    vaccine_availability_id: UUID,
    body: VaccineAvailabilityRequirementsCreateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    requirement = await VaccineAvailabilityRequirementService(db).create(
        body, api_key
    )

    if requirement == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return GeneralResponse(success=True)


@router.put(
    "/{vaccine_availability_id}/requirements/{requirement_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the id from the "
            "`vaccine_availability_id` path parameter or "
            "the requirement with the id from the "
            "`requirement_id` path parameter could not be "
            "found."
        },
    },
)
async def update_vaccine_availability_requirement(
    vaccine_availability_id: UUID,
    requirement_id: UUID,
    body: VaccineAvailabilityRequirementsUpdateRequest,
    db: MSSQLConnection = Depends(get_db),
    api_key: UUID = Depends(get_api_key),
) -> GeneralResponse:
    requirement = await VaccineAvailabilityRequirementService(db).update(
        identifier=requirement_id, params=body, auth_key=api_key
    )

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if requirement == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return GeneralResponse(success=True)
