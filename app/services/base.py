from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel

from app.db.database import MSSQLConnection
from app.services.exceptions import (
    InternalDatabaseError,
    InvalidAuthenticationKeyForRequest,
)

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
    create_procedure_name: Optional[str] = None
    update_procedure_name: Optional[str] = None
    update_procedure_id_parameter: Optional[str] = None
    delete_procedure_name: Optional[str] = None
    delete_procedure_id_parameter: Optional[str] = None

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

    async def get(
        self, identifier: Union[UUID, int], auth_key: Optional[UUID] = None
    ) -> Optional[DBResponseSchemaType]:
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

        ret_value, db_obj = await self._db.sproc_fetch_one(
            procedure_name, {procedure_id_param: identifier}, auth_key=auth_key
        )

        if db_obj is None or ret_value == -1:
            # We are assuming that any error on the stored procedure is due
            # to the fact that the object doesn't exist.
            return None

        return self.db_response_schema(**db_obj)

    async def get_multi(
        self,
    ) -> List[DBResponseSchemaType]:
        """
        List all instances from `self.table` from the database.
        """

        db_rows = await self._db.fetch_all(
            f"""
            SELECT {','.join(list(self.db_response_schema.__fields__.keys()))}
            FROM dbo.{self.table}
            """
        )

        return [self.db_response_schema(**r) for r in db_rows]

    async def create(
        self, params: CreateSchemaType, auth_key: UUID
    ) -> DBResponseSchemaType:
        """
        Creates an instance of `self.table` within the database.
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
            raise InternalDatabaseError()

        # ret_value should be the identifier for the created object
        created = await self.get(ret_value)

        if created is None:
            raise InternalDatabaseError()

        return created

    async def update(
        self,
        identifier: Union[UUID, int],
        params: UpdateSchemaType,
        auth_key: UUID,
    ) -> DBResponseSchemaType:
        """
        Updates an instance from `self.table` from the database by id.
        """

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

        parameters = params.dict(exclude={"id"})
        parameters[procedure_id_param] = identifier

        ret_value = await self._db.execute_sproc(
            procedure_name, parameters, auth_key
        )

        if ret_value == 0:
            raise InvalidAuthenticationKeyForRequest()
        elif ret_value == -1:
            raise InternalDatabaseError()

        updated = await self.get(identifier)

        if updated is None:
            raise InternalDatabaseError()

        return updated

    async def delete(
        self, identifier: Union[UUID, int], auth_key: UUID
    ) -> None:
        """
        Deletes an instance from `self.table` from the database by id.
        """

        procedure_name = (
            f"{self.table}_Delete"
            if self.delete_procedure_name is None
            else self.delete_procedure_name
        )

        procedure_id_param = (
            f"{self.table}ID"
            if self.delete_procedure_id_parameter is None
            else self.delete_procedure_id_parameter
        )

        ret_value: int = await self._db.execute_sproc(
            procedure_name, {procedure_id_param: identifier}, auth_key=auth_key
        )

        if ret_value == 0:
            raise InvalidAuthenticationKeyForRequest()
        elif ret_value == -1:
            raise InternalDatabaseError()
