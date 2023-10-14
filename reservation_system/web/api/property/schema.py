from datetime import datetime

from reservation_system.utils.base_schema import CamelBaseModel


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
