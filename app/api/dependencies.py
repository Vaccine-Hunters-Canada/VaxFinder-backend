from typing import AsyncGenerator
from app.core.config import settings
from app.db.database import MSSQLBackend, MSSQLConnection


async def get_db() -> AsyncGenerator[MSSQLConnection, None]:
    db = MSSQLBackend(settings.DB_URL)
    await db.connect()
    try:
        connection = db.connection()
        await connection.acquire(autocommit=True)
        yield connection
    finally:
        await connection.release()
        await db.disconnect()
