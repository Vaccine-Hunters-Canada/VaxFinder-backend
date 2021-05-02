from typing import List, Optional, Type
from uuid import UUID

from app.schemas.misc import FilterParamsBase
from app.schemas.vaccine_availability import (
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityResponse,
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityUpdateRequest,
)
from app.services.base import BaseService
from app.services.locations import LocationService
from app.services.organizations import OrganizationService
from loguru import logger


class VaccineAvailabilityService(
    BaseService[
        VaccineAvailabilityResponse,
        VaccineAvailabilityCreateRequest,
        VaccineAvailabilityUpdateRequest,
    ]
):
    read_procedure_id_parameter = "availabilityID"

    @property
    def table(self) -> str:
        return "vaccine_availability"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityResponse]:
        return VaccineAvailabilityResponse

    @property
    def create_response_schema(self) -> Type[VaccineAvailabilityCreateRequest]:
        return VaccineAvailabilityCreateRequest

    @property
    def update_response_schema(self) -> Type[VaccineAvailabilityUpdateRequest]:
        return VaccineAvailabilityUpdateRequest

    async def get_by_id_expanded(
        self, id: UUID
    ) -> Optional[VaccineAvailabilityExpandedResponse]:
        entry = await super().get_by_id(id)

        if entry is not None:
            location = await LocationService(self._db).get_by_id_expanded(
                entry.location
            )
            assert (
                location is not None
            ), f"Could not find location {entry.location} for entry {entry.id}"
            
            entry_expanded = entry.dict()
            entry_expanded.update({
                'location': location,
            })

            return VaccineAvailabilityExpandedResponse(
                **entry_expanded
            )

        return entry

    async def get_all_expanded(
        self, filters: Optional[FilterParamsBase] = None
    ) -> List[VaccineAvailabilityExpandedResponse]:
        entries = await super().get_all(filters=filters)
        
        logger.critical(entries)

        # TODO: should be done all at once instead of in a for loop
        entries_expanded: List[VaccineAvailabilityExpandedResponse] = []
        for entry in entries:
            location = await LocationService(self._db).get_by_id_expanded(
                entry.location
            )
            assert (
                location is not None
            ), f"Could not find location {entry.location} for entry {entry.id}"
            
            entry_expanded = entry.dict()
            entry_expanded.update({
                'location': location.dict(),
            })

            entries_expanded.append(
                VaccineAvailabilityExpandedResponse(
                    **entry_expanded
                )
            )

        return entries_expanded
