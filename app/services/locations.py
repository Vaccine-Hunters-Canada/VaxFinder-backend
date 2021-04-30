from typing import List, Union

from app.schemas.locations import LocationExpandedResponse, LocationResponse
from app.services.addresses import AddressService
from app.services.base import BaseService
from app.services.utils import convert_to_pydantic


class LocationService(BaseService):
    async def get_location_by_id(
        self, location_id: int
    ) -> LocationExpandedResponse:
        row = await self._db.fetch_one(
            f"""
                EXEC dbo.locations_Read @locationID = {location_id}
            """
        )

        if row is not None:
            locations_response: LocationResponse = convert_to_pydantic(
                LocationResponse, [row]
            )[0]
            locations_response.address = await AddressService(
                self._db
            ).get_address_by_id(locations_response.address)

            return locations_response
        return None

    async def get_locations(
        self, postal_code: str
    ) -> List[LocationExpandedResponse]:
        rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(LocationResponse.__fields__.keys()))}
                FROM dbo.locations
            """
        )

        rows: List[LocationResponse] = convert_to_pydantic(
            LocationResponse, rows
        )

        # should be done all at once instead of in a for loop
        for r in rows:
            r.address = await AddressService(self._db).get_address_by_id(
                r.address
            )

        return rows
