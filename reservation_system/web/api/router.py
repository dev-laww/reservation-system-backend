from fastapi.routing import APIRouter
from reservation_system.web.api import auth, profile, properties, tenants, payments, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["AUTH"])
api_router.include_router(profile.router, prefix="/profile", tags=["PROFILE"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["TENANTS"])
api_router.include_router(properties.router, prefix="/properties", tags=["PROPERTY"])
api_router.include_router(payments.router, prefix="/payments", tags=["PAYMENTS"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["ANALYTICS"])