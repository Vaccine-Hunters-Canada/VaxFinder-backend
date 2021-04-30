from app.core.config import settings
from app.db.database import MSSQLBackend


async def get_db():
    db = MSSQLBackend(settings.DB_URL)
    await db.connect()
    try:
        connection = db.connection()
        await connection.acquire()
        yield connection
    finally:
        await connection.release()
        await db.disconnect()
