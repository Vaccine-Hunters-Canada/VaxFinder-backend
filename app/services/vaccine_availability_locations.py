from collections import defaultdict
from datetime import date, timezone
from pprint import PrettyPrinter
from typing import Dict, List, Optional, Type
from uuid import UUID

from loguru import logger
from pydantic.types import NonNegativeInt

from app.schemas.addresses import AddressResponse
from app.schemas.locations import LocationResponse
from app.schemas.organizations import OrganizationResponse
from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityResponse,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityUpdateRequest,
    VaccineLocationExpandedResponse,
)
from app.services.base import BaseService
from app.services.exceptions import (
    DatabaseNotInSyncError,
    InternalDatabaseError,
)
from app.services.locations import LocationService
from app.services.vaccine_availability_timeslot import (
    VaccineAvailabilityTimeslotService,
)


class VaccineLocationsService(
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
    update_procedure_id_parameter = "id"
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

    # async def get_expanded(
    #     self, id: UUID
    # ) -> Optional[VaccineAvailabilityExpandedResponse]:
    #     vaccine_availability = await super().get(id)

    #     if vaccine_availability is not None:
    #         location = await LocationService(self._db).get_expanded(
    #             vaccine_availability.location
    #         )
    #         assert (
    #             location is not None
    #         ), f"""
    #             Could not find location {vaccine_availability.location}
    #             for vaccine_availability {vaccine_availability.id}
    #             """

    #         timeslots = await VaccineAvailabilityTimeslotService(
    #             self._db
    #         ).get_by_vaccine_availability_id(
    #             vaccine_availability_id=vaccine_availability.id
    #         )

    #         vaccine_availability_expanded = vaccine_availability.dict()
    #         vaccine_availability_expanded.update(
    #             {"location": location, "timeslots": timeslots}
    #         )

    #         logger.critical(vaccine_availability_expanded)

    #         return VaccineAvailabilityExpandedResponse(
    #             **vaccine_availability_expanded
    #         )

    #     return vaccine_availability

    async def get_filtered_multi_expanded(
        self, postal_code: str, min_date: date
    ) -> List[VaccineLocationExpandedResponse]:
        procedure_name = "GetVaccineLocationsNearby"

        ret_val, sproc_processed = await self._db.sproc_fetch(
            procedure_name,
            parameters={"postal": postal_code, "date": min_date},
        )

        location_rows = sproc_processed[0]
        organization_rows = sproc_processed[1]
        address_rows = sproc_processed[2]
        availability_rows = sproc_processed[3]
        timeslot_rows = sproc_processed[4]
        requirement_rows = sproc_processed[5]

        if location_rows is None:
            return []

        if (
            ret_val == -1
            or timeslot_rows is None
            or address_rows is None
            or organization_rows is None
            or requirement_rows is None
            or availability_rows is None
        ):
            raise InternalDatabaseError()

        # convert to hash tables

        # availabilities should be hashable by location
        availability_hash: Dict[
            NonNegativeInt, List[VaccineAvailabilityResponse]
        ] = defaultdict(list)
        availability_rows_valid = [
            VaccineAvailabilityResponse(**t) for t in availability_rows
        ]

        for availability_row in availability_rows_valid:
            availability_hash[availability_row.location].append(
                availability_row
            )

        # timeslots should be hashable by vaccine_availability
        timeslot_rows_valid = [
            VaccineAvailabilityTimeslotResponse(**t) for t in timeslot_rows
        ]
        timeslot_hash: Dict[
            UUID, List[VaccineAvailabilityTimeslotResponse]
        ] = defaultdict(list)
        for timeslot_row in timeslot_rows_valid:
            timeslot_hash[timeslot_row.vaccine_availability].append(
                timeslot_row
            )

        # requirements should be hashable by vaccine_availability
        requirement_rows_valid = [
            VaccineAvailabilityRequirementsResponse(**r)
            for r in requirement_rows
        ]
        requirement_hash: Dict[
            UUID, List[VaccineAvailabilityRequirementsResponse]
        ] = defaultdict(list)
        for requirement_row in requirement_rows_valid:
            requirement_hash[requirement_row.vaccine_availability].append(
                requirement_row
            )

        address_hash = {a["id"]: AddressResponse(**a) for a in address_rows}
        organization_hash = {
            o["id"]: OrganizationResponse(**o) for o in organization_rows
        }

        locations: List[VaccineLocationExpandedResponse] = []
        # expand locations
        for location_row in location_rows:
            location = LocationResponse(**location_row)

            try:
                address = address_hash[location.address]
            except KeyError:
                raise DatabaseNotInSyncError(
                    f"address `{location.address}` does not exist"
                )

            try:
                organization = organization_hash[location.organization]
            except KeyError:
                raise DatabaseNotInSyncError(
                    f"organization `{location.organization}` does not exist"
                )

            location_dict = location.dict()
            location_dict["address"] = address.dict()
            location_dict["organization"] = organization.dict()

            availabilities_list = []
            availabilities = availability_hash.get(location.id, [])
            for availability in availabilities:
                timeslots = timeslot_hash.get(availability.id, [])
                requirements = requirement_hash.get(availability.id, [])

                availability_dict = availability.dict()
                availability_dict["timeslots"] = timeslots
                availability_dict["requirements"] = requirements
                availabilities_list.append(availability_dict)

            location_dict["vaccineAvailabilities"] = availabilities_list

            locations.append(VaccineLocationExpandedResponse(**location_dict))
        return locations
