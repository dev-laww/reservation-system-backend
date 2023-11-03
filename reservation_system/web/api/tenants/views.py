from fastapi import APIRouter, Depends, Body

from ....controllers import TenantsController, NotificationController
from ....schemas.request import Notify
from ....utils.jwt import ADMIN_AUTH

router = APIRouter(dependencies=[Depends(ADMIN_AUTH)])
controller = TenantsController()
notification_controller = NotificationController()

@router.get("")
async def get_tenants():
    return await controller.get_tenants()


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: int):
    return await controller.get_tenant(tenant_id=tenant_id)


@router.post("/{tenant_id}/notifications")
async def notify_tenant(tenant_id: int, message: Notify):
    return await controller.notify_tenant(tenant_id=tenant_id, message=message, created_by="Admin")


@router.post("/notifications")
async def notify_all(message: Notify):
    return await notification_controller.notify_all(message=message, created_by="Admin")
