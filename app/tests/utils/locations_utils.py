from typing import Optional

from .db_utils import BaseDBHelper, create_sql_values_string
from .types import (
    LocationActive,
    LocationAddress,
    LocationID,
    LocationName,
    LocationNotes,
    LocationOrganization,
    LocationPhone,
    LocationPostcode,
    LocationTags,
    LocationUrl,
)


class LocationsDBHelper(BaseDBHelper):
    async def create_location(
        self,
        name: LocationName,
        active: LocationActive,
        organization: Optional[LocationOrganization] = None,
        phone: Optional[LocationPhone] = None,
        notes: Optional[LocationNotes] = None,
        address: Optional[LocationAddress] = None,
        postcode: Optional[LocationPostcode] = None,
        url: Optional[LocationUrl] = None,
        tags: Optional[LocationTags] = None,
    ) -> None:
        values_str = create_sql_values_string(
            (
                name,
                organization,
                phone,
                notes,
                address,
                active,
                postcode,
                url,
                tags,
            )
        )
        query = (
            f"INSERT INTO locations (name, organization, phone, notes, "
            f"address, active, postcode, url, tags) VALUES {values_str}"
        )

        await self._db_client.execute_query(query)
