from typing import Type

from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest
)
from app.services.base import BaseService
from loguru import logger


class OrganizationService(
    BaseService[
        OrganizationResponse, OrganizationCreateRequest, OrganizationUpdateRequest
    ]
):
    read_procedure_id_parameter = "organizationID"

    @property
    def table(self) -> str:
        return 'organizations'

    @property
    def db_response_schema(self) -> Type[OrganizationResponse]:
        return OrganizationResponse

    @property
    def create_response_schema(self) -> Type[OrganizationCreateRequest]:
        return OrganizationCreateRequest

    @property
    def update_response_schema(self) -> Type[OrganizationUpdateRequest]:
        return OrganizationUpdateRequest

    # async def create(
    #     self, full_name: str, short_name: str, description: str
    # ) -> None:
    #     await self._db.execute_stored_procedure(
    #         query="""
    #             EXEC [dbo].[organizations_Create]
    #                 @full_name=?,
    #                 @short_name=?,
    #                 @description=?;
    #         """,
    #         values=(full_name, short_name, description),
    #     )
