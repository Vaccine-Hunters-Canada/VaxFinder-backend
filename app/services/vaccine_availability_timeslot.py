from typing import List, Optional, Type, Union
from uuid import UUID

from app.schemas.misc import FilterParamsBase
from app.schemas.vaccine_availability import (
    VaccineAvailabilityTimeslotResponse,
    VaccineAvailabilityTimeslotCreateRequest,
    VaccineAvailabilityTimeslotUpdateRequest,
)
from app.services.base import BaseService
from loguru import logger


class VaccineAvailabilityTimeslotService(
    BaseService[
        VaccineAvailabilityTimeslotResponse,
        VaccineAvailabilityTimeslotCreateRequest,
        VaccineAvailabilityTimeslotUpdateRequest,
    ]
):
    read_procedure_id_parameter = "availabilityID"
    update_procedure_id_parameter = "id"

    @property
    def table(self) -> str:
        return "vaccine_availability_children"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityTimeslotResponse]:
        return VaccineAvailabilityTimeslotResponse

    @property
    def create_response_schema(self) -> Type[VaccineAvailabilityTimeslotCreateRequest]:
        return VaccineAvailabilityTimeslotCreateRequest

    @property
    def update_response_schema(self) -> Type[VaccineAvailabilityTimeslotUpdateRequest]:
        return VaccineAvailabilityTimeslotUpdateRequest

    async def get_by_id(self, identifier: Union[UUID, int]) -> None:
        raise NotImplementedError("Get by ID is not available for timeslots")

    # async def get_all(
    #     self,
    #     vaccine_availability_id: UUID,
    #     filters: Optional[FilterParamsBase] = None,
    # ) -> List[VaccineAvailabilityTimeslotResponse]:
    #     entries = await super().get_all(filters=filters)

    #     db_rows = await self._db.fetch_all(
    #         f"""
    #             SELECT
    #                 {','.join(list(self.db_response_schema.__fields__.keys()))}
    #             FROM dbo.{self.table}
    #         """
    #     )

    #     return [self.db_response_schema(**r) for r in db_rows]
