from typing import Union

from app.schemas.requirements import RequirementResponse
from app.services.base import BaseService


class RequirementService(
    BaseService[RequirementResponse, RequirementResponse, RequirementResponse]
):
    table = "requirements"
    db_response_schema = RequirementResponse
    read_procedure_id_parameter = "requirementID"
