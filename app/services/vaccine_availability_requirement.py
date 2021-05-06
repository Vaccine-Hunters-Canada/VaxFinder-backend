from typing import Type, Union
from uuid import UUID

from app.schemas.vaccine_availability import (
    VaccineAvailabilityRequirementsCreateRequest,
    VaccineAvailabilityRequirementsResponse,
    VaccineAvailabilityRequirementsUpdateRequest,
)
from app.services.base import BaseService


class VaccineAvailabilityRequirementService(
    BaseService[
        VaccineAvailabilityRequirementsResponse,
        VaccineAvailabilityRequirementsCreateRequest,
        VaccineAvailabilityRequirementsUpdateRequest,
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
    ) -> Type[VaccineAvailabilityRequirementsCreateRequest]:
        return VaccineAvailabilityRequirementsCreateRequest

    @property
    def update_response_schema(
        self,
    ) -> Type[VaccineAvailabilityRequirementsUpdateRequest]:
        return VaccineAvailabilityRequirementsUpdateRequest

    async def get(self, identifier: Union[UUID, int]) -> None:
        raise NotImplementedError(
            "Get by ID is not available for requirements"
        )

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
