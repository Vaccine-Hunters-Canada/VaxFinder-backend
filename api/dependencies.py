import os
from typing import AsyncGenerator
import uuid

from fastapi import HTTPException, Security, status, Request
from fastapi.security.api_key import APIKeyHeader
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database.database import MSSQLBackend, MSSQLConnection

async def get_db() -> AsyncGenerator[MSSQLConnection, None]:
    db = MSSQLBackend(os.environ['DATABASE_URL'])
    await db.connect()
    try:
        connection = db.connection
        await connection.acquire(autocommit=True)
        yield connection
    except Exception as e:
        logger.critical(e)
    finally:
        await connection.release()
        await db.disconnect()
