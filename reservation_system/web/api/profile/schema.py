from typing import Optional
from datetime import datetime

from reservation_system.utils.base_schema import CamelBaseModel
from reservation_system.schemas.user import User


class Profile(User):
    created_at: datetime
    updated_at: datetime


class UpdateProfile(CamelBaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    phone_number: Optional[str] = ""


class Notification(CamelBaseModel):
    id: int
    message: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class Booking(CamelBaseModel):
    id: int
    user_id: int
    property_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
