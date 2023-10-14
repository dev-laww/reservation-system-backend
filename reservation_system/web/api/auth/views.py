from fastapi import APIRouter

from reservation_system.web.api.auth import schema
from reservation_system.controllers.auth import AuthController


router = APIRouter()
controller = AuthController()


@router.post("/register", response_model=schema.AuthResponse)
async def register(data: schema.RegisterUser):
    return await controller.register(data=data)


@router.post("/login", response_model=schema.Token)
async def login(data: schema.LoginUser):
    return await controller.login(email=data.email, password=data.password)
