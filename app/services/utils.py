from typing import Any, List, Tuple, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def convert_to_pydantic(
    model: Type[T], rows: List[Tuple[Any, ...]]
) -> List[T]:
    pydantic_rows = []

    for r in rows:
        fields = {f: i for f, i in zip(model.__fields__, r)}
        pydantic_rows.append(model(**fields))

    return pydantic_rows
