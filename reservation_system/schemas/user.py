from reservation_system.utils.base_schema import CamelBaseModel


class User(CamelBaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
