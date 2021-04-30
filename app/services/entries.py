from typing import List, Union

from app.schemas.entries import EntryExpandedResponse, EntryResponse
from app.services.base import BaseService
from app.services.locations import LocationService
from app.services.utils import convert_to_pydantic


class EntryService(BaseService):
    async def get_entry_by_id(self, entry_id) -> EntryExpandedResponse:
        row = await self._db.fetch_one(
            f"""
                EXEC dbo.entries_Read @entryID = {entry_id}
            """
        )

        if row is not None:
            entry_response: EntryResponse = convert_to_pydantic(
                EntryResponse, [row]
            )[0]
            entry_response.location = await LocationService(
                self._db
            ).get_location_by_id(entry_response.location)

            return entry_response
        return None

    async def get_entries(
        self, postal_code: str
    ) -> List[EntryExpandedResponse]:
        rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(EntryResponse.__fields__.keys()))}
                FROM dbo.entries
            """
        )

        rows: List[EntryResponse] = convert_to_pydantic(EntryResponse, rows)

        # should be done all at once instead of in a for loop
        for r in rows:
            r.location = await LocationService(self._db).get_location_by_id(
                r.location
            )

        return rows
