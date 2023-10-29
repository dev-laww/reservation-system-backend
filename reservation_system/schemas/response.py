from typing import Optional

from pydantic import BaseModel

from ..utils.base_schema import CamelBaseModel


# Auth Schemas
class AuthResponse(CamelBaseModel):
    status: str
    message: str
    id: int
    admin: bool
    first_name: str
    last_name: str
    email: str


class Token(AuthResponse):
    access_token: str
    refresh_token: str


class Response(BaseModel):
    """Base response schema."""

    success: bool = True
    message: str
    data: Optional[list | dict] = None
