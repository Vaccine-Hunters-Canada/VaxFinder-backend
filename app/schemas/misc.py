from typing import Union, Literal

from pydantic import BaseModel


class GeneralResponse(BaseModel):
    success: bool
    data: Union[str, None] = None


MatchType = Literal['exact']


class FilterParamsBase(BaseModel):
    match_type: MatchType
