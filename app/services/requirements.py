from typing import Type

from app.schemas.requirements import (
    RequirementResponse,
    RequirementsCreateRequest,
    RequirementsUpdateRequest,
)
from app.services.base import BaseService


class RequirementService(
    BaseService[RequirementResponse, RequirementsCreateRequest, RequirementsUpdateRequest]
):
    read_procedure_id_parameter = "requirementID"
    delete_procedure_name = "requirements_Delete"
    delete_procedure_id_parameter = "requirementID"

    @property
    def table(self) -> str:
        return 'requirements'

    @property
    def db_response_schema(self) -> Type[RequirementResponse]:
        return RequirementResponse

    @property
    def create_response_schema(self) -> Type[RequirementsCreateRequest]:
        return RequirementsCreateRequest

    @property
    def update_response_schema(self) -> Type[RequirementsUpdateRequest]:
        return RequirementsUpdateRequest
