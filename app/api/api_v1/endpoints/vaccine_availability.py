from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_db
from app.db.database import MSSQLConnection
from app.schemas.vaccine_availability import (
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityFilterParams,
)
from app.services.vaccine_availability import VaccineAvailabilityService

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
    "/{entry_id}",
    response_model=VaccineAvailabilityExpandedResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The vaccine availability with the specified id could not be found."
        }
    },
)
async def retrieve_vaccine_availability_by_id(
    entry_id: UUID,
    db: MSSQLConnection = Depends(get_db)
) -> VaccineAvailabilityExpandedResponse:
    entry = await VaccineAvailabilityService(db).get_by_id_expanded(entry_id)

    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return entry
