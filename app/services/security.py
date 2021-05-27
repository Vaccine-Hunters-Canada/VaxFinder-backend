from typing import Type
from uuid import UUID

from app.schemas.security import (
    SecurityCreateRequest,
    SecurityLoginResponse,
    SecurityResponse,
    SecurityUpdateRequest,
)
from app.services.base import BaseService


class SecurityService(
    BaseService[SecurityResponse, SecurityCreateRequest, SecurityUpdateRequest]
):
    read_procedure_name = "Security_Read"
    read_procedure_id_parameter = "requirementID"
    create_procedure_name = "Security_Create"
    update_procedure_name = "Security_Update"
    update_procedure_id_parameter = "requirementID"
    delete_procedure_name = "Security_Delete"
    delete_procedure_id_parameter = "requirementID"

    @property
    def table(self) -> str:
        return "Security"

    @property
    def db_response_schema(self) -> Type[SecurityResponse]:
        return SecurityResponse

    @property
    def create_response_schema(self) -> Type[SecurityCreateRequest]:
        return SecurityCreateRequest

    @property
    def update_response_schema(self) -> Type[SecurityUpdateRequest]:
        return SecurityUpdateRequest

    async def Login(
        self, userName: str, password: str
    ) -> SecurityLoginResponse:
        procedure_name = "security_Login"

        ret_val, sproc_processed = await self._db.sproc_fetch(
            procedure_name,
            parameters={"userName": userName, "password": password},
        )

        if ret_val > 0:
            securityRows = sproc_processed[0]

            if securityRows is None:
                return SecurityLoginResponse(result=0)

            return SecurityLoginResponse(
                result=1, key=UUID(securityRows[0]["key"])
            )

        return SecurityLoginResponse(result=0)
