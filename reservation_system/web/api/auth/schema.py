from reservation_system.utils.base_schema import CamelBaseModel


class RegisterUser(CamelBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    password_confirmation: str


class LoginUser(CamelBaseModel):
    email: str
    password: str


class AuthResponse(CamelBaseModel):
    status: str
    message: str
    id: int
    first_name: str
    last_name: str
    email: str


class Token(AuthResponse):
    access_token: str
    refresh_token: str
