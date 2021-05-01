from typing import Optional, Type

from loguru import logger

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
    read_procedure_id_parameter = "organizationID"

    @property
    def table(self) -> str:
        return "organizations"

    @property
    def db_response_schema(self) -> Type[OrganizationResponse]:
        return OrganizationResponse

    async def create(
        self,
        full_name: Optional[str],
        short_name: str,
        description: Optional[str],
    ) -> None:
        await self._db.execute_stored_procedure(
            query="""
                EXEC [dbo].[organizations_Create]
                    @full_name=?,
                    @short_name=?,
                    @description=?;
            """,
            values=(full_name, short_name, description),
        )
