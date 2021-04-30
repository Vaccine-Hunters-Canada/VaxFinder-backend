from typing import List

from app.schemas.entries import EntryExpandedResponse, EntryResponse
from app.services.base import BaseService
from app.services.locations import LocationService


class EntryService(BaseService[EntryResponse, EntryResponse, EntryResponse]):
    table = "entries"
    db_response_schema = EntryResponse
    read_procedure_id_parameter = "entryID"

    async def get_by_id(self, id) -> EntryExpandedResponse:
        instance: EntryResponse = await super().get_by_id(id)

        if instance is not None:
            instance.location = await LocationService(self._db).get_by_id(
                instance.location
            )

        return instance

    async def get_all(self, filters=None) -> List[EntryExpandedResponse]:
        instances: List[EntryResponse] = await super().get_all(filters=filters)

        # TODO: should be done all at once instead of in a for loop
        for instance in instances:
            instance.location = await LocationService(self._db).get_by_id(
                instance.location
            )

        return instances
