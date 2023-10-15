from prisma import models

from ..utils.prisma import get_db_session


class NotificationRepository:
    prisma_client = get_db_session()

    async def get_by_id(self, notification_id: int) -> models.Notification:
        """
        Get notification by id.

        :param notification_id: notification id.
        :return: Notification.
        """
        return await self.prisma_client.notification.find_unique(
            where={"id": notification_id},
        )

    async def create(
        self,
        user_id: int,
        message: str,
        created_by: str,
    ) -> models.Notification:
        """
        Create notification.

        :param user_id: user id.
        :param message: notification message.
        :param created_by: notification creator.
        :return: Notification.
        """
        return await self.prisma_client.notification.create(
            data={
                "user_id": user_id,
                "message": message,
                "created_by": created_by,
            },
        )

    async def update(self, notification_id: int, **kwargs) -> models.Notification:
        """
        Update notification.

        :param notification_id: notification id.
        :param kwargs: notification data.
        :return: Notification.
        """
        return await self.prisma_client.notification.update(
            where={"id": notification_id},
            data=kwargs,
        )

    async def delete(self, notification_id: int) -> models.Notification:
        """
        Delete notification.

        :param notification_id: notification id.
        :return: Notification.
        """
        return await self.prisma_client.notification.delete(
            where={"id": notification_id},
        )
