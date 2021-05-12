import os
import time
from asyncio import AbstractEventLoop, get_event_loop
from functools import partial
from operator import le
from typing import AsyncGenerator, Generator, Union

import pytest
from fastapi.testclient import TestClient
from loguru import logger
from requests import Session
from toolz.functoolz import compose

from app.core.config import settings
from app.db.database import MSSQLBackend
from app.main import app

MOCK_DB_URL = "pyodbc+mssql://SA:Password0@localhost/tempdb?driver=ODBC+Driver+17+for+SQL+Server"
MAX_RETRIES = 10
VAXHUNTER_SQL_LOCATION = "vaxfinder.sql"

# We will be processing the sql file and ensuring that all statements are
# greater than this length.
MIN_SQL_QUERY_LENGTH = 4


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """
    To solve scope issues with the event loop and session-level pytest fixtures.
    Without this, async tests die with some obscure message about scope-level mismatch.
    """
    return get_event_loop()


async def connect_and_verify_db_client(db: MSSQLBackend) -> MSSQLBackend:
    """
    Connect a database client, and die if we can't.
    """
    for attempt_number in range(MAX_RETRIES):
        try:
            # check health
            await db.connect()
            logger.info("Test Database connection established")
            return db
        except Exception as e:
            logger.critical(e)
            logger.critical("Connecting to database...")
            time.sleep(5)

    raise Exception("The test database client was not able to connect.")


async def create_tables_and_sprocs(db: MSSQLBackend) -> MSSQLBackend:
    """
    Read schema file and apply it to mock SQL server instance.
    """
    connection = db.connection

    with open(VAXHUNTER_SQL_LOCATION) as sql_file:
        raw_queries = sql_file.read().split("\ngo\n")

        greater_than_min_length = partial(le, MIN_SQL_QUERY_LENGTH)
        len_greater_than_min_length = compose(greater_than_min_length, len)

        queries = filter(len_greater_than_min_length, raw_queries)

    await connection.acquire(autocommit=True)
    for query_num, query in enumerate(queries):
        try:
            await connection.execute(query)
            logger.debug(f"The {query_num}th query has succeeded.")
        except Exception as e:
            logger.error(e)
            logger.error(f"The {query_num}th query has failed.")
    await connection.release()

    return db


@pytest.fixture(scope="session")
async def db_client() -> AsyncGenerator[MSSQLBackend, None]:
    """
    Use separate DB client so we can verify the startup hook of the app
    independently.
    """
    db = MSSQLBackend(settings.DB_URL)

    db = await connect_and_verify_db_client(db)
    db = await create_tables_and_sprocs(db)

    yield db

    await db.disconnect()


@pytest.fixture(scope="module")
def app_client() -> Generator[Session, None, None]:
    with TestClient(app) as c:
        yield c
