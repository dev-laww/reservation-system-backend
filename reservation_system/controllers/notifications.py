from ..repositories import NotificationRepository
from ..utils.response import Response


class NotificationController:
    repo = NotificationRepository()

    async def notify_all(self, message: str, created_by: str):
        """
        Notify all users.

        :param message: notification message.
        :return: Notification.
        """
        await self.repo.notify_all(message=message, created_by=created_by)
        return Response.ok(
            message="Notification sent",
        )
