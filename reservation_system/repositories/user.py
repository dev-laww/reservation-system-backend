from prisma import models

from reservation_system.utils.prisma import get_db_session


class UserRepository:
    prisma_client = get_db_session()

    async def get_by_id(self, user_id: int) -> models.User:
        """
        Get user by id.

        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.user.find_unique(where={"id": user_id})

    async def get_by_email(self, email: str) -> models.User:
        """
        Get user by email.

        :param email: user email.
        :return: User.
        """
        return await self.prisma_client.user.find_unique(where={"email": email})

    async def create(self, email: str, password: str) -> models.User:
        """
        Create user.

        :param email: user email.
        :param password: user password.
        :return: User.
        """
        return await self.prisma_client.user.create(
            data={
                "email": email,
                "password": password,
            },
        )

    async def update(self, user_id: int, **kwargs) -> models.User:
        """
        Update user.

        :param user_id: user id.
        :param kwargs: user data.
        :return: User.
        """
        return await self.prisma_client.user.update(
            where={"id": user_id},
            data=kwargs,
        )

    async def delete(self, user_id: int) -> models.User:
        """
        Delete user.

        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.user.delete(where={"id": user_id})

    async def get_reviews(self, user_id: int) -> list[models.Review]:
        """
        Get user reviews.

        :param user_id: user id.
        :return: list of reviews.
        """
        return await self.prisma_client.review.find_many(where={"user_id": user_id})

    async def get_bookings(self, user_id: int) -> list[models.Booking]:
        """
        Get user bookings.

        :param user_id: user id.
        :return: list of bookings.
        """
        return await self.prisma_client.booking.find_many(where={"user_id": user_id})

    async def get_booking(self, user_id: int, booking_id: int) -> models.Booking:
        """
        Get user booking.

        :param user_id: user id.
        :param booking_id: booking id.
        :return: Booking.
        """
        return await self.prisma_client.booking.find_first(where={"id": booking_id, "user_id": user_id})

    async def cancel_booking(self, user_id: int, booking_id: int) -> models.Booking:
        """
        Cancel user booking.

        :param user_id: user id.
        :param booking_id: booking id.
        :return: Booking.
        """
        return await self.prisma_client.booking.update(
            where={
                "id": booking_id,
                "user_id": user_id,
            },
            data={"status": "CANCELLED"},
        )

    async def get_payments(self, user_id: int) -> list[models.Payment]:
        """
        Get user payments.

        :param user_id: user id.
        :return: list of payments.
        """
        return await self.prisma_client.payment.find_many(where={"user_id": user_id})

    async def get_notificaitions(self, user_id: int) -> list[models.Notification]:
        """
        Get user notifications.

        :param user_id: user id.
        :return: list of notifications.
        """
        return await self.prisma_client.notification.find_many(where={"user_id": user_id})

    async def read_notification(self, user_id: int, notification_id: int) -> models.Notification:
        """
        Read user notification.

        :param user_id: user id.
        :param notification_id: notification id.
        :return: Notification.
        """

        if not await self.prisma_client.notification.find_first(where={"id": notification_id}):
            return None

        return await self.prisma_client.notification.update(
            where={
                "id": notification_id,
                "user_id": user_id,
            },
            data={"seen": True},
        )

    async def read_all_notifications(self, user_id: int) -> list[models.Notification]:
        """
        Read all user notifications.

        :param user_id: user id.
        :return: list of notifications.
        """
        return await self.prisma_client.notification.update_many(
            where={"user_id": user_id},
            data={"seen": True},
        )

    async def get_property(self, user_id: int) -> models.Property | None:
        """
        Get user property.

        :param user_id: user id.
        :return: Property.
        """
        return await self.prisma_client.property.find_first(
            where={"user_id": user_id},
        )

    async def get_tenants(self) -> list[models.User]:
        """
        Get all tenants.

        :return: list of tenants.
        """
        return await self.prisma_client.user.find_many(
            where={"property": {"is_not": None}},
            include={"property": True},
        )

    async def get_tenant(self, user_id: int) -> models.User:
        """
        Get tenant.

        :param user_id: user id.
        :return: Tenant.
        """
        return await self.prisma_client.user.find_first(
            where={
                "id": user_id,
                "property": {"is_not": None},
            },
            include={
                "property": True,
            },
        )
