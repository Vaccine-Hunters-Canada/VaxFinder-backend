import importlib
from typing import Any, Dict, List, Optional, Tuple

import aioodbc
import sqlalchemy
from aioodbc import Connection, Pool
from databases.core import DatabaseURL
from databases.interfaces import (
    ConnectionBackend,
    DatabaseBackend,
    TransactionBackend,
)
from loguru import logger
from sqlalchemy.engine.interfaces import Dialect, ExecutionContext
from sqlalchemy.engine.result import ResultMetaData, RowProxy
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.elements import TextClause


class MSSQLBackend(DatabaseBackend):
    def __init__(
        self,
        database_url: str,
        **options: Any,
    ) -> None:
        assert len(database_url) > 0, "Missing database URL"
        self._database_url = DatabaseURL(database_url)
        self._options = options
        assert self._database_url.options.get(
            "driver"
        ), "driver parameter is not specified in database url"
        pyodbc: Any = importlib.import_module(
            f"sqlalchemy.dialects.{self._database_url.driver}.pyodbc"
        )
        assert (
            pyodbc
        ), f"Can not find pyodbc module from driver: {self._database_url.driver}"
        assert hasattr(
            pyodbc, "dialect"
        ), f"{self._database_url.driver} pyodbc does not have dialect defined."
        fast_executemany: bool = self._database_url.options.get(
            "fast_executemany", ""
        ).lower() in ["true", "yes", "1", "y", "t"]
        paramstyle: str = self._database_url.options.get("paramstyle", "qmark")
        self._dialect = pyodbc.dialect(
            paramstyle=paramstyle, fast_executemany=fast_executemany
        )
        self._options["autocommit"] = self._database_url.options.get(
            "autocommit", "false"
        ).lower() in ("true", "yes", "1", "y", "t")
        self._pool: Pool = None

    def _get_connection_kwargs(self) -> Dict[str, Any]:
        url_options = self._database_url.options

        kwargs = {}
        min_size = url_options.get("min_size")
        max_size = url_options.get("max_size")
        ssl = url_options.get("ssl")

        if min_size is not None:
            kwargs["min_size"] = int(min_size)
        if max_size is not None:
            kwargs["max_size"] = int(max_size)
        if ssl is not None:
            kwargs["ssl"] = {"true": True, "false": False}[ssl.lower()]

        kwargs.update(self._options)

        return kwargs

    @property
    def pool(self) -> Pool:
        return self._pool

    @property
    def dsn(self) -> str:
        dsn = (
            f'Driver={self._database_url.options.get("driver")}'
            f";SERVER={self._database_url.hostname}"
            f'{"," + str(self._database_url.port) if self._database_url.port is not None else ""}'
            f";DATABASE={self._database_url.database}"
            f";UID={self._database_url.username}"
            f";PWD={self._database_url.password}"
        )
        return dsn

    async def connect(self) -> None:
        assert self._pool is None, "DatabaseBackend is already running"
        kwargs = self._get_connection_kwargs()
        dsn: str = self.dsn
        self._pool = await aioodbc.create_pool(dsn=dsn, **kwargs)

    async def disconnect(self) -> None:
        assert self._pool is not None, "DatabaseBackend is not running"
        self._pool.close()
        await self._pool.wait_closed()

    def connection(self) -> "MSSQLConnection":
        return MSSQLConnection(self, self._dialect)


class CompilationContext:
    def __init__(self, context: ExecutionContext):
        self.context = context


class MSSQLConnection(ConnectionBackend):
    def __init__(self, database: MSSQLBackend, dialect: Dialect):
        self._database: MSSQLBackend = database
        self._dialect = dialect
        self._connection: Connection = None

    async def acquire(self, autocommit: bool = False) -> None:
        assert self._connection is None, "Connection is already acquired"
        assert (
            self._database.pool is not None
        ), "DatabaseBackend is not running"
        self._connection = await self._database.pool.acquire()
        self._connection._conn.autocommit = autocommit

    async def release(self) -> None:
        assert self._connection is not None, "Connection is not acquired"
        assert (
            self._database.pool is not None
        ), "DatabaseBackend is not running"
        self._connection = await self._database.pool.release(self._connection)
        self._connection = None

    async def fetch_all(self, query: ClauseElement) -> List[RowProxy]:
        assert self._connection is not None, "Connection is not acquired"
        query, args, context = self._compile(query)
        async with self._connection.cursor() as cursor:
            if args:
                await cursor.execute(query, *args)
            else:
                await cursor.execute(query)
            rows = await cursor.fetchall()
            metadata: ResultMetaData = ResultMetaData(
                context, cursor.description
            )
            return [
                RowProxy(metadata, row, metadata._processors, metadata._keymap)
                for row in rows
            ]

    async def fetch_one(self, query: ClauseElement) -> Optional[RowProxy]:
        assert self._connection is not None, "Connection is not acquired"
        query, args, context = self._compile(query)
        async with await self._connection.cursor() as cursor:
            if args:
                await cursor.execute(query, *args)
            else:
                await cursor.execute(query)
            row = await cursor.fetchone()
            if row is None:
                return None
            metadata = ResultMetaData(context, cursor.description)
            return RowProxy(
                metadata, row, metadata._processors, metadata._keymap
            )

    async def execute(self, query: ClauseElement) -> Any:
        assert self._connection is not None, "Connection is not acquired"
        query, args, context = self._compile(query)
        async with await self._connection.cursor() as cursor:
            if args:
                await cursor.execute(query, *args)
            else:
                await cursor.execute(query)
            return cursor.rowcount

    async def execute_stored_procedure(
        self, query: ClauseElement, values: Tuple[Any, ...]
    ) -> Tuple[int]:
        assert self._connection is not None, "Connection is not acquired"
        query, _, _ = self._compile(query)
        async with await self._connection.cursor() as cursor:
            await cursor.execute(query, values)
            return await cursor.fetchone()

    async def execute_many(self, queries: List[ClauseElement]) -> None:
        assert self._connection is not None, "Connection is not acquired"
        async with await self._connection.cursor() as cursor:
            for single_query in queries:
                single_query, args, context = self._compile(single_query)
                if args:
                    await cursor.execute(single_query, *args)
                else:
                    await cursor.execute(single_query)

    def transaction(self) -> "MSSQLTransaction":
        return MSSQLTransaction(self)

    def _compile(
        self, query: str
    ) -> Tuple[str, List[Any], CompilationContext]:
        sql_query: TextClause = sqlalchemy.text(query)
        compiled = sql_query.compile(dialect=self._dialect)
        args: Dict[str, Any] = compiled.construct_params()
        for key, val in args.items():
            if key in compiled._bind_processors:
                args[key] = compiled._bind_processors[key](val)

        execution_context = self._dialect.execution_ctx_cls()
        execution_context.dialect = self._dialect
        execution_context.result_column_struct = (
            compiled._result_columns,
            compiled._ordered_columns,
            compiled._textual_ordered_columns,
        )

        args_values = list(args.values())
        logger.debug(f"Query: {compiled.string}\nArgs: {args_values}")
        return (
            compiled.string,
            args_values,
            CompilationContext(execution_context),
        )

    @property
    def raw_connection(self) -> Connection:
        assert self._connection is not None, "Connection is not acquired"
        return self._connection


class MSSQLTransaction(TransactionBackend):
    def __init__(self, connection: MSSQLConnection):
        self._connection: MSSQLConnection = connection
        self._original_autocommit = self._connection.raw_connection.autocommit

    async def start(
        self, is_root: bool, extra_options: Dict[Any, Any]
    ) -> None:
        assert (
            self._connection.raw_connection is not None
        ), "Connection is not acquired"
        self._connection.raw_connection.autocommit = False

    async def commit(self) -> None:
        assert (
            self._connection.raw_connection is not None
        ), "Connection is not acquired"
        self._connection.raw_connection.commit()
        self._connection.raw_connection.autocommit = self._original_autocommit

    async def rollback(self) -> None:
        assert (
            self._connection.raw_connection is not None
        ), "Connection is not acquired"
        self._connection.raw_connection.rollback()
        self._connection.raw_connection.autocommit = self._original_autocommit
