import os
import time
from asyncio import AbstractEventLoop, get_event_loop
from functools import partial
from operator import le
from typing import AsyncGenerator, Generator, Iterable, Union

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from loguru import logger
from requests import Session
from toolz.functoolz import compose

from app.db.database import MSSQLBackend
from app.main import app
from app.tests.client.db_client import MSSQLClient, MSSQLFileGroupReader
from app.tests.settings import test_settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """
    To solve scope issues with the event loop and session-level pytest fixtures.
    Without this, async tests die with some obscure message about scope-level mismatch.
    """
    yield get_event_loop()


async def execute_sequence_of_queries(
    db: MSSQLClient,
    queries: Iterable[str],
    logger_purpose: str = "unknown purpose",
) -> MSSQLClient:
    for query_num, query in enumerate(queries):
        try:
            await db.execute_query(query)
            logger.info(
                f"The {query_num}th query for {logger_purpose} has succeeded."
            )
        except Exception as e:
            logger.error(e)
            logger.error(
                f"The {query_num}th query for {logger_purpose} has failed."
            )

    return db


async def create_tables_and_sprocs(db: MSSQLClient) -> MSSQLClient:
    """
    Read schema setup queries and apply to DB instance.
    """
    queries = MSSQLFileGroupReader().read_queries_from_folder(
        test_settings.SETUP_SQL_FILES_LOCATION
    )

    db = await execute_sequence_of_queries(db, queries, "setup")

    return db


@pytest.fixture(scope="session")
async def _db_session() -> AsyncGenerator[MSSQLClient, None]:
    """
    Use separate DB client so we can verify the startup hook of the app
    independently.
    """
    async with MSSQLClient() as test_db_client:
        test_db_client = await create_tables_and_sprocs(test_db_client)
        yield test_db_client


async def delete_all_rows(db: MSSQLClient) -> MSSQLClient:
    """
    Use preset queries to delete all data after a test case.
    """
    queries = MSSQLFileGroupReader().read_queries_from_folder(
        test_settings.AFTER_TESTCASE_SQL_FILES_LOCATION
    )

    db = await execute_sequence_of_queries(db, queries, "testcase teardown")

    return db


@pytest.fixture(scope="function")
async def db_client(
    _db_session: MSSQLClient,
) -> AsyncGenerator[MSSQLClient, None]:
    """
    Clears the DB after every use of it.
    """
    yield _db_session

    await delete_all_rows(_db_session)


@pytest.fixture(scope="session")
async def app_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testhost") as c:
        from app.db.database import db

        while True:
            try:
                # check health
                await db.connect()
                logger.info("Database connection established")
                break
            except Exception as e:
                logger.critical(e)
                logger.critical("Connecting to database...")
                time.sleep(5)
        yield c
        await db.disconnect()
