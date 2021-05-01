from app.schemas.misc import FilterParamsBase
from typing import Generic, List, Optional, Type, TypeVar
from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.db.database import MSSQLConnection

DBResponseSchemaType = TypeVar("DBResponseSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(
    ABC,
    Generic[
        DBResponseSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):

    read_procedure_name: Optional[str] = None
    read_procedure_id_parameter: Optional[str] = None

    @property
    @abstractmethod
    def table(self) -> str: pass
    
    @property
    @abstractmethod
    def db_response_schema(self) -> Type[DBResponseSchemaType]: pass

    def __init__(self, db: MSSQLConnection):
        self._db: MSSQLConnection = db

    async def get_by_id(self, id: int) -> Optional[DBResponseSchemaType]:
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

        db_row = await self._db.fetch_one(
            f"""
                EXEC dbo.{procedure_name} @{procedure_id_param} = {id}
            """
        )

        if db_row is None:
            return db_row

        return self.db_response_schema(**db_row)

    async def get_all(self, filters: Optional[FilterParamsBase] = None) -> List[DBResponseSchemaType]:
        """
        List all instances from `self.table` from the database.
        """

        db_rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(self.db_response_schema.__fields__.keys()))}
                FROM dbo.{self.table}
            """
        )

        return [self.db_response_schema(**r) for r in db_rows]
