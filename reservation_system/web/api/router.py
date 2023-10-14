from fastapi.routing import APIRouter
from reservation_system.web.api import auth, profile, tenants

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["AUTH"])
api_router.include_router(profile.router, prefix="/profile", tags=["PROFILE"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["TENANTS"])
