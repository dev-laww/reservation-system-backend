from fastapi import APIRouter

from reservation_system.web.api.auth import schema
from reservation_system.controllers.auth import AuthController


router = APIRouter()
controller = AuthController()


@router.post("/register", response_model=schema.User)
async def register(data: schema.RegisterUser):
    return await controller.register(data=data)
