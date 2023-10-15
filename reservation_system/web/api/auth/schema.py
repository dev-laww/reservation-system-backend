from pydantic import EmailStr
from reservation_system.utils.base_schema import CamelBaseModel


class RegisterUser(CamelBaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str
    password_confirmation: str


class LoginUser(CamelBaseModel):
    email: EmailStr
    password: str


class AuthResponse(CamelBaseModel):
    status: str
    message: str
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    access_token: str
    refresh_token: str


class Token(AuthResponse):
    access_token: str
    refresh_token: str


class RefreshToken(CamelBaseModel):
    refresh_token: str


class PasswordReset(CamelBaseModel):
    token: str
    password: str


class ForgotPassowrd(CamelBaseModel):
    email: str
