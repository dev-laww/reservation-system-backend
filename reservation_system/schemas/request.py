from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from ..utils.base_schema import CamelBaseModel


# Auth Schemas
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


class RefreshToken(CamelBaseModel):
    refresh_token: str


class PasswordReset(CamelBaseModel):
    token: str
    password: str


class ForgotPassowrd(CamelBaseModel):
    email: EmailStr


# Profile Schemas
class UpdateProfile(CamelBaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    phone_number: Optional[str] = ""


class ChangePassword(CamelBaseModel):
    old_password: str
    new_password: str
    confirm_password: str


# Property Schemas
class PropertyCreate(CamelBaseModel):
    name: str
    description: str
    address: str
    city: str
    state: str
    zip: str
    type: str
    price: int


class PropertyUpdate(CamelBaseModel):
    name: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    type: str = ""
    price: int = 0


class ReviewCreate(CamelBaseModel):
    rating: int
    comment: str


class ReviewUpdate(CamelBaseModel):
    rating: int = None
    comment: str = None


class RentalCreate(CamelBaseModel):
    start_date: datetime
    end_date: datetime
    payment_type: str
    amount: float


# Tenant Schemas
class Notify(CamelBaseModel):
    message: str
