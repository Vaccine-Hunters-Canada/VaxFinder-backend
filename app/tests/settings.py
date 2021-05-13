from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """
    MIN_SQL_QUERY_LENGTH: Minimum length SQL queries can be for DB setup or
    else it's rejected.

    MAX_TEST_DB_CONNECT_RETRIES: Number of times the client will retry to
    connect.

    SETUP_SQL_FILES_LOCATION: Where the SQL files for initial DB setup live.

    DB_URL: URL with all information needed for DSN.
    """

    MIN_SQL_QUERY_LENGTH: int = 4
    MAX_TEST_DB_CONNECT_RETRIES: int = 10
    SETUP_SQL_FILES_LOCATION: str = "sql/setup/"
    AFTER_TESTCASE_SQL_FILES_LOCATION: str = "sql/delete_all_rows/"
    DB_URL: str


test_settings = TestSettings()
