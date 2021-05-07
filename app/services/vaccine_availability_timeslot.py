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
    read_procedure_id_parameter = "parentID"
    create_procedure_name = "vaccine_availability_children_Create"
    update_procedure_name = "vaccine_availability_children_Update"
    update_procedure_id_parameter = "id"
    delete_procedure_name = None
    delete_procedure_id_parameter = None

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

    async def get(
        self, identifier: Union[UUID, int], auth_key: Optional[UUID] = None
    ) -> None:
        raise NotImplementedError("Get by ID is not available for timeslots")

    async def get_multi(
        self,
    ) -> List[VaccineAvailabilityTimeslotResponse]:
        raise NotImplementedError("Get multi is not available for timeslots")

    async def get_by_vaccine_availability_id(
        self, vaccine_availability_id: UUID, auth_key: Optional[UUID] = None
    ) -> Optional[List[VaccineAvailabilityTimeslotResponse]]:
        procedure_name = (
            f"{self.table}_Read"
            if self.read_procedure_name is None
            else self.read_procedure_name
        )

        ret_value, db_rows = await self._db.sproc_fetch_all(
            procedure_name,
            {self.read_procedure_id_parameter: vaccine_availability_id},
            auth_key=auth_key,
        )

        if db_rows is None:
            # We are assuming that any error on the stored procedure is due
            # to the fact that the object doesn't exist.
            return []

        if ret_value == -1:
            # We are assuming that any error on the stored procedure is due
            # to the fact that the object doesn't exist.
            raise InternalDatabaseError(f"Failed to execute {procedure_name}")

        return [VaccineAvailabilityTimeslotResponse(**o) for o in db_rows]

    async def create(
        self,
        params: VaccineAvailabilityTimeslotCreateSprocParams,
        auth_key: UUID,
    ) -> VaccineAvailabilityTimeslotResponse:
        """
        Temporary until dbo.vaccine_availability_children_ReadByParent
        sproc is applied. currently dbo.vaccine_availability_children_Read
        only takes the vaccine_availability_id, which leads to a 500 error
        when trying to query for the newly returned row.

        Instead we query for all timeslots, and then find the new one.
        """

        procedure_name = (
            f"{self.table}_Create"
            if self.create_procedure_name is None
            else self.create_procedure_name
        )

        ret_value = await self._db.execute_sproc(
            procedure_name, params.dict(), auth_key
        )

        if ret_value == 0:
            raise InvalidAuthenticationKeyForRequest()
        elif ret_value == -1:
            raise InternalDatabaseError(f"Failed to execute {procedure_name}")

        all_timeslots = await self.get_by_vaccine_availability_id(
            params.parentID
        )

        if all_timeslots is None:
            raise InternalDatabaseError()

        created = next(
            (t for t in all_timeslots if t.id == UUID(ret_value)), None
        )

        if created is None:
            raise InternalDatabaseError()

        return created
