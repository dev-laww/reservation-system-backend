from reservation_system.utils.base_schema import CamelBaseModel


class Notify(CamelBaseModel):
    message: str
