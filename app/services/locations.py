from app.services.organizations import OrganizationService
from app.schemas.misc import FilterParamsBase
from typing import List, Optional, Type

from loguru import logger

from app.schemas.locations import (
    LocationExpandedResponse,
    LocationResponse,
    LocationCreateRequest,
    LocationUpdateRequest,
)
from app.services.addresses import AddressService
from app.services.base import BaseService


class LocationService(
    BaseService[LocationResponse, LocationCreateRequest, LocationUpdateRequest]
):
    read_procedure_id_parameter = "locationID"

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


    async def get_by_id_expanded(
        self, id: int
    ) -> Optional[LocationExpandedResponse]:
        location = await super().get_by_id(id)

        if location is not None:
            address = await AddressService(self._db).get_by_id(
                location.address
            )

            assert (
                address is not None
            ), f'Could not find address {location.address} for location {location.id}'
                 
            organization = await OrganizationService(self._db).get_by_id(
                location.organization
            )

            assert (
                organization is not None
            ), f'Could not find organization {location.organization} for location {location.id}'
            
            location_expanded = location.dict()
            location_expanded.update({
                'address': address,
                'organization': organization
            })
            
            logger.critical(location_expanded)

            return LocationExpandedResponse(**location_expanded)

        return location

    async def get_all_expanded(
        self, filters: Optional[FilterParamsBase] = None
    ) -> List[LocationExpandedResponse]:
        locations = await super().get_all(filters)

        # TODO: should be done all at once instead of in a for loop
        locations_expanded: List[LocationExpandedResponse] = []
        for location in locations:
            address = await AddressService(self._db).get_by_id(
                location.address
            )

            assert (
                address is not None
            ), f'Could not find address {location.address} for location {location.id}'
            
            organization = await OrganizationService(self._db).get_by_id(
                location.organization
            )

            assert (
                organization is not None
            ), f'Could not find organization {location.organization} for location {location.id}'

            location_expanded = location.dict()
            location_expanded.update({
                'address': address,
                'organization': organization
            })

            locations_expanded.append(LocationExpandedResponse(**location_expanded))

        return locations_expanded
