from fastapi import APIRouter, Depends
from reservation_system.controllers.auth import AuthController
from reservation_system.utils.jwt import AUTH
from reservation_system.schemas.token import JWTData
from reservation_system.web.api.auth import schema

router = APIRouter()
controller = AuthController()


@router.post("/register", response_model=schema.AuthResponse)
async def register(data: schema.RegisterUser):
    return await controller.register(data=data)


@router.post("/login", response_model=schema.Token)
async def login(data: schema.LoginUser):
    return await controller.login(email=data.email, password=data.password)


@router.post("/refresh")
async def refresh_token(refresh: schema.RefreshToken, user: JWTData = Depends(AUTH)):
    return await controller.refresh_token(user_id=user.id, refresh_token=refresh.refresh_token)


@router.post("/forgot-password")
async def forgot_password(data: schema.ForgotPassowrd):
    return await controller.forgot_password(data=data)


@router.post("/reset-password")
async def reset_password(data: schema.PasswordReset):
    return await controller.reset_password(data=data)
