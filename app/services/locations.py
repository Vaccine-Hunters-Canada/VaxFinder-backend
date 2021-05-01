from typing import List, Optional
from loguru import logger

from app.schemas.locations import LocationExpandedResponse, LocationResponse
from app.services.addresses import AddressService
from app.services.base import BaseService


class LocationService(
    BaseService[LocationResponse, LocationResponse, LocationResponse]
):
    table = "locations"
    db_response_schema = LocationResponse
    read_procedure_id_parameter = "locationID"

    async def get_by_id(self, id) -> LocationExpandedResponse:
        instance: LocationResponse = await super().get_by_id(id)

        if instance is not None:
            instance.address = await AddressService(self._db).get_by_id(
                instance.address
            )

        return instance

    async def get_all(self, filters=None) -> List[LocationExpandedResponse]:
        instances: List[LocationResponse] = await super().get_all(filters)

        # TODO: should be done all at once instead of in a for loop
        for instance in instances:
            instance.address = await AddressService(self._db).get_by_id(
                instance.address
            )

        return instances
