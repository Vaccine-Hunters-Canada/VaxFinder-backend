from humps import camelize
from pydantic import BaseModel as PydanticBaseModel


def to_camel(convert_str: str) -> str:
    return str(camelize(convert_str))


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        use_enum_values = True
