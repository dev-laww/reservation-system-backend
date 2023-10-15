from reservation_system.repositories.notification import NotificationRepository
from reservation_system.repositories.user import UserRepository
from reservation_system.schemas.profile import Notification
from reservation_system.schemas.user import Tenant
from reservation_system.utils.responses import Error, SuccessResponse


class TenantController:
    repo = UserRepository()
    notif_repo = NotificationRepository()

    async def get_tenant(self, tenant_id: int):
        """
        Get tenant by id.

        :param tenant_id: tenant id.
        :return: Tenant.
        """
        tenant = await self.repo.get_tenant(user_id=tenant_id)

        if not tenant:
            raise Error.NOT_FOUND

        return SuccessResponse(
            message="Tenant retrieved", data=Tenant(**tenant.model_dump()).model_dump()
        )

    async def get_tenants(self):
        """
        Get all tenants.

        :return: Tenants.
        """

        tenants = await self.repo.get_tenants()

        return SuccessResponse(
            message="Tenants retrieved",
            data=[Tenant(**tenant.model_dump()).model_dump() for tenant in tenants],
        )

    async def notify_tenant(self, tenant_id: int, message: str):
        """
        Notify tenant.

        :param tenant_id: tenant id.
        :param message: notification message.
        :return: Notification.
        """

        tenant = await self.repo.get_tenant(user_id=tenant_id)

        if not tenant:
            raise Error.NOT_FOUND

        notification = await self.notif_repo.create(
            user_id=tenant_id,
            message=message,
            created_by="System",
        )

        return SuccessResponse(
            message="Tenant notified",
            data=Notification(**notification.model_dump()).model_dump(),
        )
