import asyncio
import time
from functools import partial
from operator import le
from os import listdir
from os.path import isdir, isfile, join
from types import TracebackType
from typing import Any, Iterable, Optional, Type

import aioodbc
from databases.core import DatabaseURL
from loguru import logger
from toolz import compose

from app.tests.settings import test_settings
from app.tests.utils.utils import (
    Location,
    get_number_in_str,
    read_content_from_file,
)


class TestMSSQLClient:
    """
    A quick and dirty SQL client for the mock SQL Server instance that will
    be used for integration testing.

    This is meant to be used as an async context manager, ie.
    with TestMSSQLClient() as client:
        client.execute_query(...)
        ...
    """

    def __init__(
        self, db_url: str = test_settings.DB_URL, autocommit: bool = True
    ) -> None:
        # Construct DSN. Force Usage of SQL Server 17
        database_url = DatabaseURL(db_url)
        self._dsn: str = (
            f'Driver={database_url.options.get("driver")}'
            f";SERVER={database_url.hostname}"
            f'{"," + str(database_url.port) if database_url.port is not None else ""}'
            f";DATABASE={database_url.database}"
            f";UID={database_url.username}"
            f";PWD={database_url.password}"
        )

        self._event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self._pool: Optional[aioodbc.pool.Pool] = None

        self._autocommit: bool = autocommit

    @property
    def pool(self) -> Optional[aioodbc.pool.Pool]:
        return self._pool

    async def execute_query(self, query: str) -> None:
        assert self._pool is not None
        async with self._pool.acquire() as connection:
            async with connection.cursor() as cur:
                await cur.execute(query)

    async def fetch_all(self, query: str) -> Any:
        assert self._pool is not None
        async with self._pool.acquire() as connection:
            async with connection.cursor() as cur:
                await cur.execute(query)
                rows = await cur.fetchall()

        return rows

    async def __aenter__(self) -> "TestMSSQLClient":
        logger.debug("Verifying MSSQL client connection...")

        for attempt_number in range(test_settings.MAX_TEST_DB_CONNECT_RETRIES):
            try:
                if self._pool is None:
                    self._pool = await aioodbc.create_pool(
                        dsn=self._dsn,
                        loop=self._event_loop,
                        autocommit=self._autocommit,
                    )

                async with self._pool.acquire() as connection:
                    async with connection.cursor() as cur:
                        pass
                logger.debug("Test MSSQL client created.")
                return self
            except Exception as e:
                logger.critical(e)
                logger.critical("Connecting to database...")
                time.sleep(5)

        raise Exception(
            "The test database client was not able to connect. Is the database running?"
        )

    async def __aexit__(
        self,
        exc_type: Type[Optional[BaseException]],
        exc: Optional[BaseException],
        tb: TracebackType,
    ) -> None:
        assert self._pool is not None
        self._pool.close()
        await self._pool.wait_closed()
        logger.debug("Test MSSQL client closed.")


class MSSQLFileGroupReader:
    """
    A utility class for reading in SQL files for sequential execution. It sorts
    them according to their sequence number in their filenames.
    """

    def __init__(
        self, min_query_length: int = test_settings.MIN_SQL_QUERY_LENGTH
    ):
        self.min_query_length = min_query_length

    def read_queries_from_folder(self, dir_path: Location) -> Iterable[str]:
        assert isdir(dir_path)

        all_files_in_folder = listdir(dir_path)

        is_sql_file = (
            lambda filename: isfile(join(dir_path, filename))
            and filename[-4:].lower() == ".sql"
        )

        create_full_path = partial(join, dir_path)

        # Need to sort by sequence number in filename
        sql_files_in_folder = sorted(
            map(create_full_path, filter(is_sql_file, all_files_in_folder)),
            key=get_number_in_str,
        )

        raw_queries = map(read_content_from_file, sql_files_in_folder)

        greater_than_min_length = partial(
            le, test_settings.MIN_SQL_QUERY_LENGTH
        )
        len_greater_than_min_length = compose(greater_than_min_length, len)

        queries: Iterable[str] = filter(
            len_greater_than_min_length, raw_queries
        )

        return queries
