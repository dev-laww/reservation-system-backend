from typing import Optional

from reservation_system.utils.base_schema import CamelBaseModel


class UpdateProfile(CamelBaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    phone_number: Optional[str] = ""


class ChangePassword(CamelBaseModel):
    old_password: str
    new_password: str
    confirm_password: str
