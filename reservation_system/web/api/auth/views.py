from fastapi import APIRouter, Depends

from ....controllers import AuthController
from ....schemas import request, response, token
from ....utils.jwt import AUTH

router = APIRouter()
controller = AuthController()


@router.post("/register", response_model=response.AuthResponse)
async def register(data: request.RegisterUser):
    return await controller.register(data=data)


@router.post("/login", response_model=response.Token)
async def login(data: request.LoginUser):
    return await controller.login(email=data.email, password=data.password)


@router.post("/refresh")
async def refresh_token(
    refresh: request.RefreshToken
):
    return await controller.refresh_token(
        refresh_token=refresh.refresh_token
    )


@router.post("/forgot-password")
async def forgot_password(data: request.ForgotPassowrd):
    return await controller.forgot_password(data=data)


@router.post("/reset-password")
async def reset_password(data: request.PasswordReset):
    return await controller.reset_password(data=data)
