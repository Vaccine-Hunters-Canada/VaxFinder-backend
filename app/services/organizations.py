from typing import Union

from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
)
from app.services.base import BaseService


class OrganizationService(
    BaseService[
        OrganizationResponse, OrganizationCreateRequest, OrganizationResponse
    ]
):
    table = "organizations"
    db_response_schema = OrganizationResponse
    read_procedure_id_parameter = "organizationID"

    async def create(
        self, full_name: str, short_name: str, description: str
    ) -> Union[OrganizationResponse, None]:
        await self._db.execute_stored_procedure(
            query="""
                EXEC [dbo].[organizations_Create]
                    @full_name=?,
                    @short_name=?,
                    @description=?;
            """,
            values=(full_name, short_name, description),
        )
