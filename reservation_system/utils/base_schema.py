from pydantic import BaseModel, ConfigDict

from reservation_system.utils.alias import to_camel


class CamelBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
