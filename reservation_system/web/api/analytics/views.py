from fastapi import APIRouter
from ....controllers import AnalyticsController

router = APIRouter()
analytics_controller = AnalyticsController()

@router.get("/payments")
async def get_analytics(year: int, month: int):
    return await analytics_controller.get_all_payments(year=year, month=month)
