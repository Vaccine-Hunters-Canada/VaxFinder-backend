from typing import List, Optional, Type

from app.schemas.locations import (
    LocationCreateRequest,
    LocationExpandedResponse,
    LocationResponse,
    LocationUpdateRequest,
)
from app.services.addresses import AddressService
from app.services.base import BaseService
from app.services.organizations import OrganizationService


class LocationService(
    BaseService[LocationResponse, LocationCreateRequest, LocationUpdateRequest]
):
    read_procedure_name = "locations_Read"
    read_procedure_id_parameter = "locationID"
    create_procedure_name = "locations_Create"
    update_procedure_name = "locations_Update"
    update_procedure_id_parameter = "locationID"
    delete_procedure_name = "locations_Delete"
    delete_procedure_id_parameter = "locationID"

    @property
    def table(self) -> str:
        return "locations"

    @property
    def db_response_schema(self) -> Type[LocationResponse]:
        return LocationResponse

    @property
    def create_response_schema(self) -> Type[LocationCreateRequest]:
        return LocationCreateRequest

    @property
    def update_response_schema(self) -> Type[LocationUpdateRequest]:
        return LocationUpdateRequest

    async def _expand(
        self, location: LocationResponse
    ) -> LocationExpandedResponse:
        address = None
        if location.address is not None:
            address = await AddressService(self._db).get(location.address)
            assert (
                address is not None
            ), f"Could not find address {location.address} for location {location.id}"

        organization = None
        if location.organization is not None:
            organization = await OrganizationService(self._db).get(
                location.organization
            )
            assert (
                organization is not None
            ), f"Could not find organization {location.organization} for location {location.id}"

        location_expanded = location.dict()
        location_expanded.update(
            {"address": address, "organization": organization}
        )

        return LocationExpandedResponse(**location_expanded)

    async def get_expanded(
        self, id: int
    ) -> Optional[LocationExpandedResponse]:
        location = await super().get(id)

        if location is not None:
            return await self._expand(location=location)

        return location

    async def get_expanded_key(
        self, externalKey: str
    ) -> Optional[LocationExpandedResponse]:
        

        procedure_name = "locations_ReadByExternalKey"

        ret_val, sproc_processed = await self._db.sproc_fetch(
            procedure_name,
            parameters={
                "external_key": externalKey
            },
        )

        location_rows = sproc_processed[0]   
        location = LocationResponse(**location_rows[0])
        
        if location is not None:
            return await self._expand(location=location)

        return location

    async def get_multi_expanded(self) -> List[LocationExpandedResponse]:
        locations = await super().get_multi()

        # TODO: should be done all at once instead of in a for loop
        locations_expanded: List[LocationExpandedResponse] = []

        for location in locations:
            address = None
            if location.address is not None:
                address = await AddressService(self._db).get(location.address)
                assert (
                    address is not None
                ), f"Could not find address {location.address} for location {location.id}"

            organization = None
            if location.organization is not None:
                organization = await OrganizationService(self._db).get(
                    location.organization
                )
                assert organization is not None, (
                    f"Could not find organization {location.organization} for "
                    f"location {location.id}"
                )

            location_expanded = location.dict()
            location_expanded.update(
                {"address": address, "organization": organization}
            )

            locations_expanded.append(
                LocationExpandedResponse(**location_expanded)
            )

        return locations_expanded
