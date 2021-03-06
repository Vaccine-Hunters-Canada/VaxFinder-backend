from typing import Type

from app.schemas.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from app.services.base import BaseService


class OrganizationService(
    BaseService[
        OrganizationResponse,
        OrganizationCreateRequest,
        OrganizationUpdateRequest,
    ]
):
    read_procedure_name = "organizations_Read"
    read_procedure_id_parameter = "organizationID"
    create_procedure_name = "organizations_Create"
    update_procedure_name = "organizations_Update"
    update_procedure_id_parameter = "organizationID"
    delete_procedure_name = "organizations_Delete"
    delete_procedure_id_parameter = "organizationID"

    @property
    def table(self) -> str:
        return "organizations"

    @property
    def db_response_schema(self) -> Type[OrganizationResponse]:
        return OrganizationResponse

    @property
    def create_response_schema(self) -> Type[OrganizationCreateRequest]:
        return OrganizationCreateRequest

    @property
    def update_response_schema(self) -> Type[OrganizationUpdateRequest]:
        return OrganizationUpdateRequest
