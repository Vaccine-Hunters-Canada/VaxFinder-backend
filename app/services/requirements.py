from typing import Type

from app.schemas.requirements import RequirementResponse
from app.services.base import BaseService


class RequirementService(
    BaseService[RequirementResponse, RequirementResponse, RequirementResponse]
):
    read_procedure_id_parameter = "requirementID"
    
    @property
    def table(self) -> str:
        return 'requirements'

    @property
    def db_response_schema(self) -> Type[RequirementResponse]:
        return RequirementResponse
