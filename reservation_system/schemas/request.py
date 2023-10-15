from datetime import datetime
from typing import Optional

from ..utils.base_schema import CamelBaseModel


# Auth Schemas
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
    max_occupancy: int


class PropertyUpdate(CamelBaseModel):
    name: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    type: str = ""
    price: int = 0
    max_occupancy: int = 0


class ReviewCreate(CamelBaseModel):
    rating: int
    comment: str


class ReviewUpdate(CamelBaseModel):
    rating: int = None
    comment: str = None


class BookingCreate(CamelBaseModel):
    start_date: datetime
    end_date: datetime


# Tenant Schemas
class Notify(CamelBaseModel):
    message: str
