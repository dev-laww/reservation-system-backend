from fastapi import APIRouter

from ....controllers import AuthController
from ....schemas import request, response

router = APIRouter()
controller = AuthController()


@router.post("/register", response_model=response.AuthResponse)
async def register(data: request.RegisterUser):
    return await controller.register(data=data)


@router.post("/login", response_model=response.Token)
async def login(data: request.LoginUser):
    return await controller.login(email=data.email, password=data.password)
