from ..repositories import NotificationRepository, UserRepository
from ..schemas.profile import Notification
from ..schemas.request import Notify
from ..schemas.user import Tenant
from ..utils.response import Response


class TenantsController:
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
            raise Response.not_found(message="Tenant not found")

        return Response.ok(
            message="Tenant retrieved",
            data=Tenant(**{**tenant.model_dump(), "property": tenant.tenant_property.property.model_dump()}).model_dump(),
        )

    async def get_tenants(self):
        """
        Get all tenants.

        :return: Tenants.
        """

        tenants = await self.repo.get_tenants()

        return Response.ok(
            message="Tenants retrieved",
            data=[Tenant(**{**tenant.model_dump(), "property": tenant.tenant_property.property.model_dump()}).model_dump() for tenant in tenants],
        )

    async def notify_tenant(self, tenant_id: int, message: Notify):
        """
        Notify tenant.

        :param tenant_id: tenant id.
        :param message: notification message.
        :return: Notification.
        """

        tenant = await self.repo.get_tenant(user_id=tenant_id)

        if not tenant:
            raise Response.not_found(message="Tenant not found")

        notification = await self.notif_repo.create(
            user_id=tenant_id,
            message=message.message,
            created_by="System",
        )

        return Response.ok(
            message="Tenant notified",
            data=Notification(**notification.model_dump()).model_dump(),
        )
