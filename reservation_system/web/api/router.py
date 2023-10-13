from fastapi.routing import APIRouter
from reservation_system.web.api import echo, monitoring, auth

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])