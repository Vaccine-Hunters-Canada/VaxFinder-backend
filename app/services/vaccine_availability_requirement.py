from typing import List, Optional, Type, Union
from uuid import UUID

from app.schemas.misc import FilterParamsBase
from app.schemas.vaccine_availability import (
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityRequirementsCreateRequest,
    VaccineAvailabilityRequirementsUpdateRequest,
)
from app.services.base import BaseService
from loguru import logger


class VaccineAvailabilityRequirementService(
    BaseService[
        VaccineAvailabilityRequirementsResponse,
        VaccineAvailabilityRequirementsCreateRequest,
        VaccineAvailabilityRequirementsUpdateRequest,
    ]
):
    read_procedure_id_parameter = "availabilityID"
    update_procedure_id_parameter = "id"

    @property
    def table(self) -> str:
        return "vaccine_availability_requirements"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityRequirementsResponse]:
        return VaccineAvailabilityRequirementsResponse

    @property
    def create_response_schema(self) -> Type[VaccineAvailabilityRequirementsCreateRequest]:
        return VaccineAvailabilityRequirementsCreateRequest

    @property
    def update_response_schema(self) -> Type[VaccineAvailabilityRequirementsUpdateRequest]:
        return VaccineAvailabilityRequirementsUpdateRequest

    async def get_by_id(self, identifier: Union[UUID, int]) -> None:
        raise NotImplementedError('Get by ID is not available for requirements')

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
