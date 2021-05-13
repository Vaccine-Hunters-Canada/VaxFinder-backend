import asyncio
import os
import time
from pathlib import Path
from types import TracebackType
from typing import Any, Optional, Type

import aioodbc
from databases.core import DatabaseURL
from loguru import logger

from app.tests.settings import test_settings


class TestMSSQLClient:
    def __init__(self, db_url: str = test_settings.DB_URL) -> None:
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

    @property
    def pool(self) -> Optional[aioodbc.pool.Pool]:
        return self._pool

    async def execute_query(self, query: str) -> Any:
        assert self._pool is not None
        async with self._pool.acquire() as connection:
            async with connection.cursor() as cur:
                await cur.execute(query)
                return cur.rowcount

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
                        dsn=self._dsn, loop=self._event_loop
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
