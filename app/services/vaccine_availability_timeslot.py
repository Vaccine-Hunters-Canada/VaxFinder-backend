from typing import List, Optional, Type, Union
from uuid import UUID

from loguru import logger

from app.schemas.vaccine_availability import (
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotCreateSprocParams,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotUpdateRequest,
)
from app.services.base import BaseService
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)


class VaccineAvailabilityTimeslotService(
    BaseService[
        VaccineAvailabilityTimeslotResponse,
        VaccineAvailabilityTimeslotCreateSprocParams,
        VaccineAvailabilityTimeslotUpdateRequest,
    ]
):
    read_procedure_name = None
    read_procedure_id_parameter = "id"
    create_procedure_name = "vaccine_availability_children_Create"
    update_procedure_name = "vaccine_availability_children_Update"
    update_procedure_id_parameter = "id"
    delete_procedure_name = "vaccine_availability_children_Delete"
    delete_procedure_id_parameter = "id"

    @property
    def table(self) -> str:
        return "vaccine_availability_children"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityTimeslotResponse]:
        return VaccineAvailabilityTimeslotResponse

    @property
    def create_response_schema(
        self,
    ) -> Type[VaccineAvailabilityTimeslotCreateSprocParams]:
        return VaccineAvailabilityTimeslotCreateSprocParams

    @property
    def update_response_schema(
        self,
    ) -> Type[VaccineAvailabilityTimeslotUpdateRequest]:
        return VaccineAvailabilityTimeslotUpdateRequest

    async def get_multi(
        self,
    ) -> List[VaccineAvailabilityTimeslotResponse]:
        raise NotImplementedError("Get multi is not available for timeslots")

    async def get_by_vaccine_availability_id(
        self, vaccine_availability_id: UUID, auth_key: Optional[UUID] = None
    ) -> Optional[List[VaccineAvailabilityTimeslotResponse]]:
        procedure_name = "vaccine_availability_children_ReadByParent"

        ret_value, db_rows = await self._db.sproc_fetch_all(
            procname=procedure_name,
            parameters={"parentID": vaccine_availability_id},
            auth_key=auth_key,
        )

        if db_rows is None:
            # We are assuming that any error on the stored procedure is due
            # to the fact that the object doesn't exist.
            return []

        if ret_value == -1:
            raise InternalDatabaseError(f"Failed to execute {procedure_name}")

        return [VaccineAvailabilityTimeslotResponse(**o) for o in db_rows]
