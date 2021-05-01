from typing import List, Optional, Type

from app.schemas.misc import FilterParamsBase
from app.schemas.vaccine_availability import (
    VaccineAvailabilityExpandedResponse, VaccineAvailabilityResponse)
from app.services.base import BaseService
from app.services.locations import LocationService


class VaccineAvailabilityService(
    BaseService[
        VaccineAvailabilityResponse,
        VaccineAvailabilityResponse,
        VaccineAvailabilityResponse,
    ]
):
    read_procedure_id_parameter = "availabilityID"

    @property
    def table(self) -> str:
        return "vaccine_availability"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityResponse]:
        return VaccineAvailabilityResponse

    async def get_by_id_expanded(
        self, id: int
    ) -> Optional[VaccineAvailabilityExpandedResponse]:
        entry = await super().get_by_id(id)

        if entry is not None:
            location = await LocationService(self._db).get_by_id_expanded(
                entry.location
            )
            assert (
                location is not None
            ), f"Could not find location {entry.location} for entry {entry.id}"
            if location is not None:
                entry_expanded = VaccineAvailabilityExpandedResponse(
                    **entry.dict(), location=location
                )
                return entry_expanded

        return entry

    async def get_all_expanded(
        self, filters: Optional[FilterParamsBase] = None
    ) -> List[VaccineAvailabilityExpandedResponse]:
        entries = await super().get_all(filters=filters)

        # TODO: should be done all at once instead of in a for loop
        entries_expanded: List[VaccineAvailabilityExpandedResponse] = []
        for entry in entries:
            location = await LocationService(self._db).get_by_id_expanded(
                entry.location
            )
            assert (
                location is not None
            ), f"Could not find location {entry.location} for entry {entry.id}"
            entries_expanded.append(
                VaccineAvailabilityExpandedResponse(
                    **entry.dict(), location=location
                )
            )

        return entries_expanded
