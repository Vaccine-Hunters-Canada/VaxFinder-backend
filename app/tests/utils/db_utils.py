from functools import reduce
from typing import Any, Callable, Tuple

from app.tests.client.db_client import MSSQLClient

NULL_STR = "NULL"


def create_sql_values_string(values: Tuple[Any, ...]) -> str:
    """
    Given a tuple of Pythonic values to be used in a SQL query,
    concatenate them together into a string that will used as the values
    tuple for a SQL query.
    Ex. Given (1, "Location0", "1112223333"), we will turn that into the
    string "(1, 'Location0', '1112223333')"
    """
    assert len(values) > 0

    convert_to_null_if_none = (
        lambda value: f"{repr(value)}" if value else NULL_STR
    )
    sql_compatible_values = tuple(map(convert_to_null_if_none, values))

    add_value_to_string: Callable[[str, str], str] = (
        lambda current_str, next_value: current_str + f", {next_value}"
    )

    return f"({reduce(add_value_to_string, sql_compatible_values)})"


class BaseDBHelper:
    def __init__(self, _db_client: MSSQLClient):
        self._db_client: MSSQLClient = _db_client
