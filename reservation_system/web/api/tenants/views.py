from fastapi import APIRouter, Depends
from reservation_system.controllers.tenants import TenantController
from reservation_system.utils.jwt import ADMIN_AUTH
from reservation_system.web.api.tenants.schema import Notify

router = APIRouter(dependencies=[Depends(ADMIN_AUTH)])
controller = TenantController()


@router.get("")
async def get_tenants():
    return await controller.get_tenants()


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: int):
    return await controller.get_tenant(tenant_id=tenant_id)


@router.post("/{tenant_id}/notifications")
async def notify_tenant(tenant_id: int, message: Notify):
    return await controller.notify_tenant(tenant_id=tenant_id, message=message)
