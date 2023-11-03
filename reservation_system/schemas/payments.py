from typing import Optional

from .property import Rental
from .user import User
from ..utils.base_schema import CamelBaseModel


class Payments(CamelBaseModel):
    id: int
    user_id: int
    rental_id: int
    amount: float
    type: str
    status: str
    user: User
    rental: Optional[Rental]
