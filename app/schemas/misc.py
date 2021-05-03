from typing import Union, Literal

from pydantic import BaseModel


class GeneralResponse(BaseModel):
    success: bool
    data: Union[str, None] = None


MatchType = Literal[
    "exact", "list"  # input 1, output 1  # input multiple, output multiple
]


class FilterParamsBase(BaseModel):
    match_type: MatchType
