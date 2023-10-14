from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Base response schema."""

    success: bool = True
    message: str
    data: dict
