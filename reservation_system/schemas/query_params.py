from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class CommonQuery(BaseModel):
    limit: int = 100
    offset: int = Query(default=0, ge=0)


class PropertyQuery(CommonQuery):
    min_price: int = Query(default=0, ge=0)
    max_price: Optional[int] = Query(default=None, ge=0)
    price: Optional[int] = Query(default=None, ge=0)
    min_occupancy: int = Query(default=0, ge=0)
    max_occupancy: Optional[int] = Query(default=None, ge=0)
    occupancy: Optional[int] = Query(default=None, ge=0)
    sort: Optional[str] = Query(default=None)
    order: Optional[str] = Query(default=None, regex="^(asc|desc)$")
