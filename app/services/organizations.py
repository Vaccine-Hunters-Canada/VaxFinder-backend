from typing import List, Union

from app.schemas.organizations import (OrganizationCreateRequest,
                                       OrganizationResponse)
from app.services.base import BaseService
from app.services.utils import convert_to_pydantic


class OrganizationService(BaseService):

    async def get_organization_by_id(
        self, organization_id: int
    ) -> OrganizationResponse:
        row = await self._db.fetch_one(
            f"""
                EXEC dbo.organizations_Read @organizationID = {organization_id}
            """
        )

        if row is not None:
            organizations_response: OrganizationResponse = (
                convert_to_pydantic(OrganizationResponse, [row])[0]
            )

            return organizations_response
        return None

    async def get_organizations(
        self, name: str
    ) -> List[OrganizationResponse]:
        rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(OrganizationResponse.__fields__.keys()))}
                FROM dbo.organizations
            """
        )

        rows: List[OrganizationResponse] = convert_to_pydantic(
            OrganizationResponse, rows
        )

        return rows

    async def create_organization(
        self, full_name: str, short_name: str, description: str
    ) -> Union[OrganizationResponse, None]:
        return await self._db.execute(
            f"""EXEC dbo.organizations_Create
                    @full_name = '{full_name}',
                    @short_name = '{short_name}',
                    @description = '{description}'
            """
        )
