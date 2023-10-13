from reservation_system.utils.base_schema import CamelBaseModel


class RegisterUser(CamelBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    password_confirmation: str


class User(CamelBaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
