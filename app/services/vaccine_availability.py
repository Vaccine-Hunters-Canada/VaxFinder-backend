from collections import defaultdict
from datetime import date, timezone
from pprint import PrettyPrinter
from typing import Dict, List, Optional, Type
from uuid import UUID

from loguru import logger
from pywebpush import webpush

from app.schemas.addresses import AddressResponse
from app.schemas.locations import LocationResponse
from app.schemas.organizations import OrganizationResponse
from app.schemas.vaccine_availability import (
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityExpandedCreateRequest,
    VaccineAvailabilityExpandedCreateResponse,
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityResponse,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityUpdateRequest,
)
from app.services.base import BaseService
from app.services.discord import discordCallNoDoses, discordCallReport
from app.services.exceptions import (
    DatabaseNotInSyncError,
    InternalDatabaseError,
)
from app.services.locations import LocationService
from app.services.vaccine_availability_requirement import (
    VaccineAvailabilityRequirementService,
)
from app.services.vaccine_availability_timeslot import (
    VaccineAvailabilityTimeslotService,
)
from app.services.webPush import WebPushService


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

    async def get_expanded(
        self, id: UUID
    ) -> Optional[VaccineAvailabilityExpandedResponse]:
        vaccine_availability = await super().get(id)

        if vaccine_availability is not None:
            location = await LocationService(self._db).get_expanded(
                vaccine_availability.location
            )
            assert (
                location is not None
            ), f"""
                Could not find location {vaccine_availability.location}
                for vaccine_availability {vaccine_availability.id}
                """

            timeslots = await VaccineAvailabilityTimeslotService(
                self._db
            ).get_by_vaccine_availability_id(
                vaccine_availability_id=vaccine_availability.id
            )

            requirements = await VaccineAvailabilityRequirementService(
                self._db
            ).get_by_vaccine_availability_id(
                vaccine_availability_id=vaccine_availability.id
            )

            vaccine_availability_expanded = vaccine_availability.dict()
            vaccine_availability_expanded.update(
                {
                    "location": location,
                    "timeslots": timeslots,
                    "requirements": requirements,
                }
            )

            logger.critical(vaccine_availability_expanded)

            return VaccineAvailabilityExpandedResponse(
                **vaccine_availability_expanded
            )

        return vaccine_availability

    async def get_filtered_multi_expanded(
        self, postal_code: str, min_date: date
    ) -> List[VaccineAvailabilityExpandedResponse]:
        procedure_name = "GetAvailableVaccines"

        ret_val, sproc_processed = await self._db.sproc_fetch(
            procedure_name,
            parameters={"postal": postal_code, "date": min_date},
        )

        availability_rows = sproc_processed[0]
        timeslot_rows = sproc_processed[1]
        requirement_rows = sproc_processed[2]
        location_rows = sproc_processed[3]
        address_rows = sproc_processed[4]
        organization_rows = sproc_processed[5]

        if availability_rows is None:
            return []

        if (
            ret_val == -1
            or timeslot_rows is None
            or location_rows is None
            or address_rows is None
            or organization_rows is None
            or requirement_rows is None
        ):
            raise InternalDatabaseError()

        # convert to hash tables
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

        location_hash = {l["id"]: LocationResponse(**l) for l in location_rows}
        address_hash = {a["id"]: AddressResponse(**a) for a in address_rows}
        organization_hash = {
            o["id"]: OrganizationResponse(**o) for o in organization_rows
        }

        # expand availabilities
        availabilities: List[VaccineAvailabilityExpandedResponse] = []

        for availability_row in availability_rows:
            availability = VaccineAvailabilityResponse(**availability_row)

            timeslots = timeslot_hash.get(availability.id, [])
            requirements = requirement_hash.get(availability.id, [])

            try:
                location = location_hash[availability.location]
            except KeyError:
                raise DatabaseNotInSyncError(
                    f"location `{availability.location}` does not exist"
                )

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
            availability_dict = availability.dict()
            availability_dict["timeslots"] = timeslots
            availability_dict["requirements"] = requirements
            availability_dict["location"] = location_dict
            availabilities.append(
                VaccineAvailabilityExpandedResponse(**availability_dict)
            )
        return availabilities

    async def get_by_location(
        self, locationID: int, min_date: date
    ) -> List[VaccineAvailabilityResponse]:
        procedure_name = "vaccine_availability_ReadByLocation"

        ret_val, sproc_processed = await self._db.sproc_fetch(
            procedure_name,
            parameters={"locationID": locationID, "date": min_date},
        )

        availability_rows = sproc_processed[0]

        if availability_rows is None:
            return []

        if ret_val == -1:
            raise InternalDatabaseError()

        # expand availabilities
        availabilities: List[VaccineAvailabilityResponse] = []

        for availability_row in availability_rows:
            availability = VaccineAvailabilityResponse(**availability_row)

            availabilities.append(
                VaccineAvailabilityResponse(**availability.dict())
            )
        return availabilities

    async def create_expanded(
        self,
        va_expanded: VaccineAvailabilityExpandedCreateRequest,
        locationID: Optional[int],
        external_key: Optional[str],
        auth_key: UUID,
    ) -> VaccineAvailabilityExpandedCreateResponse:
        procedure_name = "vaccine_availability_expanded_Create"

        parameters = {
            "numberAvailable": va_expanded.numberAvailable,
            "numberTotal": va_expanded.numberTotal,
            "date": va_expanded.date,
            "vaccine": va_expanded.vaccine,
            "inputType": va_expanded.inputType,
            "tagsA": va_expanded.tagsA,
            "line1": va_expanded.line1,
            "line2": va_expanded.line2,
            "city": va_expanded.city,
            "province": va_expanded.province,
            "postcode": va_expanded.postcode,
            "name": va_expanded.name,
            "organization": va_expanded.organization,
            "phone": va_expanded.phone,
            "notes": va_expanded.notes,
            "active": va_expanded.active,
            "url": va_expanded.url,
            "tagsL": va_expanded.tagsL,
            "external_key": external_key,
        }

        if locationID is not None:
            if locationID > 0:
                parameters.update({"location": locationID})

        if external_key is not None:
            parameters.update({"external_key": external_key})

        ret_value, sproc_processed = await self._db.sproc_fetch(
            procedure_name, parameters, auth_key=auth_key
        )

        if ret_value < 0:
            raise InternalDatabaseError()

        availability_rows = sproc_processed[0]

        if availability_rows is None or availability_rows[0] is None:
            raise InternalDatabaseError()

        availability_rows[0]["response_code"] = ret_value

        resp = VaccineAvailabilityExpandedCreateResponse(
            **availability_rows[0]
        )

        if ret_value > 0:
            if va_expanded.numberAvailable > 0:
                wpservice = WebPushService(self._db)
                await WebPushService.SendWebpush(
                    wpservice, va_expanded.postcode, locationID
                )

        # if ret_value > 0:
        #    if va_expanded.numberAvailable > 0:
        #        discordCallReport(va_expanded)
        #    else:
        #        discordCallNoDoses(va_expanded)

        return resp
