from app.db.database import MSSQLConnection


class BaseService:
    def __init__(self, db: MSSQLConnection):
        self._db = db
