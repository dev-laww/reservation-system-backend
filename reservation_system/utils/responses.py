from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Base response schema."""

    success: bool = True
    message: str
    data: Optional[list | dict] = None


class Error:
    not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    forbidden = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    bad_request = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
