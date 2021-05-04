from typing import Type, Union
from uuid import UUID

from app.schemas.vaccine_availability import (
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotUpdateRequest,
)
from app.services.base import BaseService


class VaccineAvailabilityTimeslotService(
    BaseService[
        VaccineAvailabilityTimeslotResponse,
        VaccineAvailabilityTimeslotCreateRequest,
        VaccineAvailabilityTimeslotUpdateRequest,
    ]
):
    read_procedure_name = None
    read_procedure_id_parameter = None
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
    ) -> Type[VaccineAvailabilityTimeslotCreateRequest]:
        return VaccineAvailabilityTimeslotCreateRequest

    @property
    def update_response_schema(
        self,
    ) -> Type[VaccineAvailabilityTimeslotUpdateRequest]:
        return VaccineAvailabilityTimeslotUpdateRequest

    async def get(self, identifier: Union[UUID, int]) -> None:
        raise NotImplementedError("Get by ID is not available for timeslots")

    # async def get_multi(
    #     self,
    #     vaccine_availability_id: UUID,
    # ) -> List[VaccineAvailabilityTimeslotResponse]:
    #     entries = await super().get_multi()

    #     db_rows = await self._db.fetch_all(
    #         f"""
    #             SELECT
    #                 {','.join(list(self.db_response_schema.__fields__.keys()))}
    #             FROM dbo.{self.table}
    #         """
    #     )

    #     return [self.db_response_schema(**r) for r in db_rows]
