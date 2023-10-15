from fastapi import HTTPException, status

from ..repositories import UserRepository
from ..schemas.profile import Profile
from ..schemas.request import ChangePassword, UpdateProfile
from ..utils.hashing import check_password, hash_password
from ..utils.response import Response


class ProfileController:
    repo = UserRepository()

    async def get_profile(self, user_id: int):
        """
        Get user profile.

        :param user_id: user id.
        :return: User profile.
        """
        user = await self.repo.get_by_id(user_id=user_id)

        return Response.ok(
            message="Profile retrieved",
            data=Profile(**user.model_dump()).model_dump(),
        )

    async def update_profile(self, user_id: int, data: UpdateProfile):
        """
        Update user profile.

        :param user_id: user id.
        :param data: user data.
        :return: User profile.
        """
        user = await self.repo.update(
            user_id=user_id, **{k: v for k, v in data.model_dump().items() if v}
        )

        return Response.ok(
            message="Profile updated",
            data=Profile(**user.model_dump()).model_dump(),
        )

    async def change_password(self, user_id: int, data: ChangePassword):
        """
        Change user password.

        :return: User profile.
        """

        user = await self.repo.get_by_id(user_id=user_id)

        if not check_password(data.old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        if data.new_password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match",
            )

        password = hash_password(data.new_password)

        user_updated = await self.repo.update(user_id=user_id, password=password)

        return Response.ok(
            message="Password updated",
            data=Profile(**user_updated.model_dump()).model_dump(),
        )

    async def get_notifications(self, user_id: int):
        """
        Get user notifications.

        :return: User notifications.
        """

        notifications = await self.repo.get_notifications(user_id=user_id)

        return Response.ok(
            message="Notifications retrieved",
            data=[notification.model_dump() for notification in notifications],
        )

    async def mark_read(self, user_id: int, notification_id: int):
        """
        Mark notification as read.

        :param notification_id: notification id.
        :param user_id: user id.
        :return: User notifications.
        """

        notification = await self.repo.read_notification(
            user_id=user_id,
            notification_id=notification_id,
        )

        if not notification:
            raise Response.not_found(message="Notification not found")

        return Response.ok(
            message="Notification marked as read",
            data=notification.model_dump(),
        )

    async def mark_all_read(self, user_id: int):
        """
        Mark all notifications as read.

        :param user_id: user id.
        :return: User notifications.
        """

        await self.repo.read_all_notifications(user_id=user_id)
        return Response.ok(
            message="Notifications marked as read",
        )

    async def get_bookings(self, user_id: int):
        """
        Get user bookings.

        :param user_id: user id.
        :return: User bookings.
        """

        bookings = await self.repo.get_bookings(user_id=user_id)

        return Response.ok(
            message="Bookings retrieved",
            data=[booking.model_dump() for booking in bookings],
        )

    async def get_booking(self, user_id: int, booking_id: int):
        """
        Get user booking.

        :param user_id: user id.
        :param booking_id: booking id.
        :return: User booking.
        """

        booking = await self.repo.get_booking(user_id=user_id, booking_id=booking_id)

        if not booking:
            raise Response.not_found(message="Booking not found")

        return Response.ok(
            message="Booking retrieved",
            data=booking.model_dump(),
        )

    async def cancel_booking(self, user_id: int, booking_id: int):
        """
        Cancel user booking.

        :param user_id: user id.
        :param booking_id: booking id.
        :return: User booking.
        """

        booking = await self.repo.cancel_booking(user_id=user_id, booking_id=booking_id)

        if not booking:
            raise Response.not_found(message="Booking not found")

        return Response.ok(
            message="Booking cancelled",
            data=booking.model_dump(),
        )
