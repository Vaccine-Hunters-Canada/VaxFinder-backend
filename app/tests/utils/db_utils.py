from abc import ABC, abstractmethod
from functools import reduce
from typing import Any, Callable, Tuple

from loguru import logger

from app.tests.client.db_client import MSSQLClient

NULL_STR = "NULL"


def create_sql_values_string(values: Tuple[Any, ...]) -> str:
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
