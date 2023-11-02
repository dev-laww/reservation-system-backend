from datetime import datetime

from ..schemas.user import User
from ..utils.base_schema import CamelBaseModel


class Profile(User):
    created_at: datetime
    updated_at: datetime


class Notification(CamelBaseModel):
    id: int
    message: str
    created_by: str
    created_at: datetime


class Rental(CamelBaseModel):
    id: int
    user_id: int
    property_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
