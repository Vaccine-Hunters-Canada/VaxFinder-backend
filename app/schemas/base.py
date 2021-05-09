from datetime import datetime, timezone

from humps import camelize
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator


def to_camel(convert_str: str) -> str:
    return str(camelize(convert_str))


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        use_enum_values = True

    @validator("created_at", pre=True, check_fields=False)
    def _date_to_utc(cls, dt: datetime) -> datetime:
        if dt is not None and isinstance(dt, datetime):
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
