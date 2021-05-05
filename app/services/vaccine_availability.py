from typing import List, Optional, Type
from uuid import UUID
from datetime import datetime
from loguru import logger

from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityResponse,
    VaccineAvailabilityUpdateRequest,
)
from app.services.base import BaseService
from app.services.locations import LocationService


class VaccineAvailabilityService(
    BaseService[
        VaccineAvailabilityResponse,
        VaccineAvailabilityCreateRequest,
        VaccineAvailabilityUpdateRequest,
    ]
):
    read_procedure_name = "vaccine_availability_Read"
    read_procedure_id_parameter = "availabilityID"
    create_procedure_name = "vaccine_availability_Create"
    update_procedure_name = "vaccine_availability_Update"
    update_procedure_id_parameter = "entryID"
    delete_procedure_name = "vaccine_availability_Delete"
    delete_procedure_id_parameter = "avaliabilityID"

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

    async def _expand(
        self, vaccine_availability: VaccineAvailabilityResponse
    ) -> VaccineAvailabilityExpandedResponse:
        location = await LocationService(self._db).get_expanded(
            vaccine_availability.location
        )
        assert (
            location is not None
        ), f"""
            Could not find location {vaccine_availability.location}
            for vaccine_availability {vaccine_availability.id}
            """

        vaccine_availability_expanded = vaccine_availability.dict()
        vaccine_availability_expanded.update(
            {
                "location": location,
            }
        )

        # logger.critical(vaccine_availability_expanded)

        return VaccineAvailabilityExpandedResponse(
            **vaccine_availability_expanded
        )

    async def get_expanded(
        self, id: UUID
    ) -> Optional[VaccineAvailabilityExpandedResponse]:
        vaccine_availability = await super().get(id)

        if vaccine_availability is not None:
            return await self._expand(
                vaccine_availability=vaccine_availability
            )

        return vaccine_availability

    async def get_multi_filtered(
        self,
        postal_code: str,
        min_date: datetime
    ) -> Optional[List[VaccineAvailabilityExpandedResponse]]:
        _, rows = await self._db.sproc_fetch_all(
            procname='GetAvailableVaccines',
            parameters={
                'postal': postal_code,
                'date': min_date
            },
            auth_key=None
        )

        if rows is not None:
            vaccine_availabilities = [VaccineAvailabilityResponse(**r) for r in rows]
            vaccine_availabilities_expanded: List[
                VaccineAvailabilityExpandedResponse
            ] = []
            for vaccine_availability in vaccine_availabilities:
                vaccine_availabilities_expanded.append(
                    await self._expand(vaccine_availability)
                )
            return vaccine_availabilities_expanded
        return rows
        

    async def get_multi_expanded(
        self,
    ) -> List[VaccineAvailabilityExpandedResponse]:
        vaccine_availabilities = await super().get_multi()

        # TODO: should be done all at once instead of in a for loop
        vaccine_availabilities_expanded: List[
            VaccineAvailabilityExpandedResponse
        ] = []
        for vaccine_availability in vaccine_availabilities:
            vaccine_availabilities_expanded.append(
                await self._expand(vaccine_availability)
            )

        return vaccine_availabilities_expanded
