from typing import Union, Literal

from pydantic import BaseModel


class GeneralResponse(BaseModel):
    success: bool
    data: Union[str, None] = None

MatchType = Literal[
    'exact', # input 1, output 1
    'list' # input multiple, output multiple
]


class FilterParamsBase(BaseModel):
    match_type: MatchType
