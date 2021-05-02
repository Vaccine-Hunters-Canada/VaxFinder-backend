from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel

from app.db.database import MSSQLConnection
from app.schemas.misc import FilterParamsBase

DBResponseSchemaType = TypeVar("DBResponseSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(
    ABC,
    Generic[
        DBResponseSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ],
):
    read_procedure_name: Optional[str] = None
    read_procedure_id_parameter: Optional[str] = None
    update_procedure_id_parameter: Optional[str] = None
    create_procedure_name: Optional[str] = None
    update_procedure_name: Optional[str] = None

    @property
    @abstractmethod
    def table(self) -> str:
        pass

    @property
    @abstractmethod
    def db_response_schema(self) -> Type[DBResponseSchemaType]:
        pass

    @property
    @abstractmethod
    def create_response_schema(self) -> Type[CreateSchemaType]:
        pass

    @property
    @abstractmethod
    def update_response_schema(self) -> Type[UpdateSchemaType]:
        pass

    def __init__(self, db: MSSQLConnection):
        self._db: MSSQLConnection = db

    async def get_by_id(self, identifier: Union[UUID, int]) -> Optional[
        DBResponseSchemaType]:
        """
        Retrieve an instance from `self.table` from the database by id. None if
        the object can't be found.
        """

        procedure_name = (
            f"{self.table}_Read"
            if self.read_procedure_name is None
            else self.read_procedure_name
        )

        procedure_id_param = (
            f"{self.table}ID"
            if self.read_procedure_id_parameter is None
            else self.read_procedure_id_parameter
        )

        if isinstance(identifier, UUID):
            identifier: str = f"'{identifier}'"  # type: ignore

        db_row = await self._db.fetch_one(
            f"""
                EXEC dbo.{procedure_name} @{procedure_id_param} = {identifier}
            """
        )

        if db_row is None:
            return db_row

        return self.db_response_schema(**db_row)

    async def get_all(
        self,
        filters: Optional[FilterParamsBase] = None,
    ) -> List[DBResponseSchemaType]:
        """
        List all instances from `self.table` from the database.
        """

        filter_query = ''
        if filters is not None:
            filters_dict = filters.dict()
            filter_match_type = filters_dict.pop('match_type')
            filters_no_blank = {k: v for k, v in filters_dict.items() if v}
            if filters_no_blank:
                db_filters = []
                for k, v in filters_dict.items():
                    if isinstance(v, UUID) or isinstance(v, str):
                        v = f"'{v}'"
                    db_filters.append(f'{k}={v}')
                filter_query = f" WHERE {' AND '.join(db_filters)}"

        db_rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(self.db_response_schema.__fields__.keys()))}
                FROM dbo.{self.table}
                {filter_query} 
            """
        )

        return [self.db_response_schema(**r) for r in db_rows]

    async def create(self, params: CreateSchemaType, auth_key: UUID) -> None:
        procedure_name = (
            f"{self.table}_Create"
            if self.create_procedure_name is None
            else self.create_procedure_name
        )

        db_params = ["@auth=?"] + [
            f'@{k}=?'
            for k in
            self.create_response_schema.__fields__.keys()
        ]

        await self._db.execute_stored_procedure(
            query=f"""
                EXEC dbo.{procedure_name}
                    {','.join(db_params)}
            """,
            values=(tuple([auth_key] + list(params.dict().values()))),
        )

    async def update(
        self,
        identifier: Union[UUID, int],
        params: UpdateSchemaType,
        auth_key: UUID
    ) -> Optional[int]:
        # exists = await self.get_by_id(id)

        # if exists is None:
        #     return None

        procedure_name = (
            f"{self.table}_Update"
            if self.update_procedure_name is None
            else self.update_procedure_name
        )

        procedure_id_param = (
            f"{self.table}ID"
            if self.update_procedure_id_parameter is None
            else self.update_procedure_id_parameter
        )

        db_params = ["@auth=?"] + [
            f'@{k}=?'
            for k in
            self.update_response_schema.__fields__.keys()
        ]

        if isinstance(identifier, UUID):
            identifier: str = f"'{identifier}'"  # type: ignore

        db_params.append(f'@{procedure_id_param}={identifier}')

        resp: int = await self._db.execute_stored_procedure(
            query=f"""
                EXEC dbo.{procedure_name}
                    {','.join(db_params)}
            """,
            values=(tuple([auth_key] + list(params.dict().values()))),
        )

        return resp
