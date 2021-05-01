from pydantic import BaseModel
from typing import Union, Literal

class GeneralResponse(BaseModel):
    success: bool
    data: Union[str, None] = None

MatchType = Literal['exact']

class FilterParamsBase(BaseModel):
    match_type: MatchType
