from datetime import datetime
from typing import Optional

from ..utils.base_schema import CamelBaseModel
from .user import User


class PropertyImage(CamelBaseModel):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime


class Review(CamelBaseModel):
    id: int
    property_id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime
    user: Optional[User]


class Property(CamelBaseModel):
    id: int
    name: str
    description: str
    price: int
    type: str
    address: str
    city: str
    state: str
    zip: str
    occupied: bool
    created_at: datetime
    updated_at: datetime
    images: list[PropertyImage]
    reviews: list[Review]
    tenant: Optional[User]


class Rental(CamelBaseModel):
    id: int
    user_id: int
    property_id: int
    start_date: datetime
    end_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
