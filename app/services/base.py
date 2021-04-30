from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

from app.db.database import MSSQLConnection
from app.services.utils import convert_to_pydantic

DBResponseSchemaType = TypeVar("DBResponseSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(
    Generic[
        DBResponseSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    table: Optional[str] = None
    db_response_schema: Optional[DBResponseSchemaType] = None
    read_procedure_name: Optional[str] = None
    read_procedure_id_parameter: Optional[str] = None

    def __init__(self, db: MSSQLConnection):
        self._db: MSSQLConnection = db

    def _check_attributes_set(self):
        assert (
            self.table is not None
        ), f"{self.__class__.__name__} should include a `table` attribute."
        assert (
            self.db_response_schema is not None
        ), f"{self.__class__.__name__} should include a `db_response_schema` attribute."

    async def get_by_id(self, id) -> Type[DBResponseSchemaType]:
        """
        Retrieve an instance from `self.table` from the database by id. None if
        the object can't be found.
        """
        self._check_attributes_set()

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

        return convert_to_pydantic(self.db_response_schema, [db_row])[0]

    async def get_all(self, filters=None) -> Type[List[DBResponseSchemaType]]:
        """
        List all instances from `self.table` from the database.
        """
        self._check_attributes_set()

        db_rows = await self._db.fetch_all(
            f"""
                SELECT
                    {','.join(list(self.db_response_schema.__fields__.keys()))}
                FROM dbo.{self.table}
            """
        )

        pydantic_rows: List[DBResponseSchemaType] = convert_to_pydantic(
            self.db_response_schema, db_rows
        )

        return pydantic_rows
