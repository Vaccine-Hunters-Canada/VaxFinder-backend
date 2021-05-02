from app.schemas.misc import GeneralResponse
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityFilterParams,
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotFilterParams,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotUpdateRequest,
    VaccineAvailabilityUpdateRequest,
)
from app.services.vaccine_availability import VaccineAvailabilityService
from app.services.vaccine_availability_timeslot import VaccineAvailabilityTimeslotService

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
            "description": "The vaccine availability with the specified id could not be found."
        }
    },
)
async def retrieve_vaccine_availability_by_id(
    vaccine_availability_id: UUID,
    db: MSSQLConnection = Depends(get_db)
) -> VaccineAvailabilityExpandedResponse:
    entry = await VaccineAvailabilityService(db).get_by_id_expanded(vaccine_availability_id)

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry

@router.post("", response_model=GeneralResponse)
async def create_vaccine_availability(
    body: VaccineAvailabilityCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> GeneralResponse:
    await VaccineAvailabilityService(db).create(body)

    return GeneralResponse(success=True)

@router.put(
    "/{vaccine_availability_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def update_vaccine_availability(
    vaccine_availability_id: int,
    body: VaccineAvailabilityUpdateRequest,
    db: MSSQLConnection = Depends(get_db)
) -> GeneralResponse:
    requirement = await VaccineAvailabilityService(db).update(
        id=vaccine_availability_id,
        params=body)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GeneralResponse(success=True)

@router.get(
    "/{vaccine_availability_id}/timeslots",
    response_model=List[VaccineAvailabilityTimeslotResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id could not be found."
        }
    },
) 
async def retrieve_vaccine_availability_timeslots_by_id(
    vaccine_availability_id: UUID,
    db: MSSQLConnection = Depends(get_db)
) -> List[VaccineAvailabilityTimeslotResponse]:
    entry = await VaccineAvailabilityTimeslotService(db).get_all(
        VaccineAvailabilityTimeslotFilterParams(
            vaccine_availability=vaccine_availability_id,
            match_type='exact'
        )
    )

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry

@router.post("/{vaccine_availability_id}/timeslots", response_model=GeneralResponse)
async def create_vaccine_availability_timeslot(
    body: VaccineAvailabilityTimeslotCreateRequest,
    db: MSSQLConnection = Depends(get_db),
) -> GeneralResponse:
    await VaccineAvailabilityTimeslotService(db).create(body)

    return GeneralResponse(success=True)

@router.put(
    "/{vaccine_availability_id}/timeslots/{timeslot_id}",
    response_model=GeneralResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The location with the specified id could not be found."
        }
    },
)
async def update_vaccine_availability_timeslot(
    timeslot_id: UUID,
    body: VaccineAvailabilityTimeslotUpdateRequest,
    db: MSSQLConnection = Depends(get_db)
) -> GeneralResponse:
    requirement = await VaccineAvailabilityTimeslotService(db).update(
        id=timeslot_id,
        params=body)

    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GeneralResponse(success=True)
