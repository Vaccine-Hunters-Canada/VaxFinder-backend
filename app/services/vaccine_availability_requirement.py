from datetime import datetime
from typing import List, Optional, Type, Union
from uuid import UUID

from loguru import logger

from app.schemas.vaccine_availability import (
    VaccineAvailabilityRequirementCreateRequest,
    VaccineAvailabilityRequirementCreateSprocParams,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityRequirementUpdateRequest,
)
from app.services.base import BaseService
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)


class VaccineAvailabilityRequirementService(
    BaseService[
        VaccineAvailabilityRequirementsResponse,
        VaccineAvailabilityRequirementCreateSprocParams,
        VaccineAvailabilityRequirementUpdateRequest,
    ]
):
    read_procedure_name = None
    read_procedure_id_parameter = None
    create_procedure_name = "vaccine_availability_requirements_Create"
    update_procedure_name = "vaccine_availability_requirements_Update"
    update_procedure_id_parameter = "id"
    delete_procedure_name = None
    delete_procedure_id_parameter = None

    @property
    def table(self) -> str:
        return "vaccine_availability_requirements"

    @property
    def db_response_schema(
        self,
    ) -> Type[VaccineAvailabilityRequirementsResponse]:
        return VaccineAvailabilityRequirementsResponse

    @property
    def create_response_schema(
        self,
    ) -> Type[VaccineAvailabilityRequirementCreateSprocParams]:
        return VaccineAvailabilityRequirementCreateSprocParams

    @property
    def update_response_schema(
        self,
    ) -> Type[VaccineAvailabilityRequirementUpdateRequest]:
        return VaccineAvailabilityRequirementUpdateRequest

    async def get(
        self, identifier: Union[UUID, int], auth_key: Optional[UUID] = None
    ) -> None:
        raise NotImplementedError(
            "Get by ID is not available for requirements"
        )

    async def get_multi(
        self,
    ) -> List[VaccineAvailabilityRequirementsResponse]:
        raise NotImplementedError("Get multi is not available for timeslots")

    # async def get_by_vaccine_availability_id(
    #     self,
    #     vaccine_availability_id: UUID,
    #     auth_key: Optional[UUID] = None
    # ) -> Optional[List[VaccineAvailabilityRequirementsResponse]]:
    #     procedure_name = (
    #         f"{self.table}_Read"
    #         if self.read_procedure_name is None
    #         else self.read_procedure_name
    #     )

    #     ret_value, db_rows = await self._db.sproc_fetch_all(
    #         procedure_name,
    #         {f"{self.table}ID": vaccine_availability_id},
    #         auth_key=auth_key
    #     )

    #     if db_rows is None:
    #         # We are assuming that any error on the stored procedure is due
    #         # to the fact that the object doesn't exist.
    #         return []

    #     if ret_value == -1:
    #         # We are assuming that any error on the stored procedure is due
    #         # to the fact that the object doesn't exist.
    #         raise InternalDatabaseError(
    #             f'Failed to execute {procedure_name}'
    #         )

    #     return [
    #         VaccineAvailabilityRequirementsResponse(**o)
    #         for o in db_rows
    #     ]

    async def create(
        self,
        params: VaccineAvailabilityRequirementCreateSprocParams,
        auth_key: UUID,
    ) -> VaccineAvailabilityRequirementsResponse:
        """
        Temporary until dbo.vaccine_availability_requirement_ReadByParent
        and dbo.vaccine_availability_requirement_Read sproc is applied.
        """

        procedure_name = (
            f"{self.table}_Create"
            if self.create_procedure_name is None
            else self.create_procedure_name
        )

        ret_value = await self._db.execute_sproc(
            procedure_name, params.dict(), auth_key
        )
        logger.critical(ret_value)

        if ret_value == 0:
            raise InvalidAuthenticationKeyForRequest()
        elif ret_value == -1:
            raise InternalDatabaseError(f"Failed to execute {procedure_name}")

        # all_timeslots = await self.get_by_vaccine_availability_id(
        #     params.parentID
        # )

        # if all_timeslots is None:
        #     raise InternalDatabaseError()

        # created = next((t for t in all_timeslots if t.id == UUID(ret_value)), None)

        # if created is None:
        #     raise InternalDatabaseError()

        return VaccineAvailabilityRequirementsResponse(
            id=1,
            vaccine_availability=params.vaccine_availability,
            requirement=1,
            active=True,
            created_at=datetime.now(),
        )
