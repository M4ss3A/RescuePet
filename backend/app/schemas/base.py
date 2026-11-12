from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base de los schemas: en el JSON los campos viajan en camelCase (edadAproximada),
    mientras que en Python se usan en snake_case (edad_aproximada)."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)