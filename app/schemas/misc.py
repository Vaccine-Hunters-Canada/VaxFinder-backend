from pydantic import BaseModel
from typing import Union

class General_Response(BaseModel):
    success: bool
    data: Union[str, None] = None
