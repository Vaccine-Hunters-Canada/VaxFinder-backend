from typing import List, Union

from app.schemas.addresses import AddressResponse
from app.services.base import BaseService
from app.services.utils import convert_to_pydantic


class AddressService(BaseService):
    async def get_address_by_id(
        self, address_id: int
    ) -> Union[AddressResponse, None]:
        row = await self._db.fetch_one(
            f"""
                EXEC dbo.address_Read @addressID = {address_id}
            """
        )

        if row is not None:
            address_response: AddressResponse = convert_to_pydantic(
                AddressResponse, [row]
            )[0]

            return address_response
        return None

    async def get_addresses(self, postal_code: str) -> List[AddressResponse]:
        rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(AddressResponse.__fields__.keys()))}
                FROM dbo.address
            """
        )

        pydantic_rows: List[AddressResponse] = convert_to_pydantic(
            AddressResponse, rows
        )

        return pydantic_rows
