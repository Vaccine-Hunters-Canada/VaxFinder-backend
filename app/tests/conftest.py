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
from app.tests.client.db_client import TestMSSQLClient
from app.tests.settings import test_settings

VAXHUNTER_SQL_LOCATION = "vaxfinder.sql"


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """
    To solve scope issues with the event loop and session-level pytest fixtures.
    Without this, async tests die with some obscure message about scope-level mismatch.
    """
    return get_event_loop()


async def create_tables_and_sprocs(db: TestMSSQLClient) -> TestMSSQLClient:
    """
    Read schema file and apply it to mock SQL server instance.
    """
    with open(VAXHUNTER_SQL_LOCATION) as sql_file:
        raw_queries = sql_file.read().split("\ngo\n")

        greater_than_min_length = partial(
            le, test_settings.MIN_SQL_QUERY_LENGTH
        )
        len_greater_than_min_length = compose(greater_than_min_length, len)

        queries = tuple(filter(len_greater_than_min_length, raw_queries))

    for query_num, query in enumerate(queries):
        try:
            await db.execute_query(query)
            logger.info(f"The {query_num}th query has succeeded.")
        except Exception as e:
            logger.error(e)
            logger.error(f"The {query_num}th query has failed.")

    return db


@pytest.fixture(scope="session")
async def db_client() -> AsyncGenerator[TestMSSQLClient, None]:
    """
    Use separate DB client so we can verify the startup hook of the app
    independently.
    """
    async with TestMSSQLClient() as test_db_client:
        test_db_client = await create_tables_and_sprocs(test_db_client)
        yield test_db_client


@pytest.fixture(scope="module")
def app_client() -> Generator[Session, None, None]:
    with TestClient(app) as c:
        yield c
