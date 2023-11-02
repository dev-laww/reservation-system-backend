from fastapi import APIRouter, Depends

from ....controllers import ProfileController
from ....schemas import request
from ....schemas.token import JWTData
from ....utils.jwt import AUTH

router = APIRouter()
controller = ProfileController()


@router.get("")
async def get_profile(user: JWTData = Depends(AUTH)):
    return await controller.get_profile(user_id=user.id)


@router.put("")
async def update_profile(data: request.UpdateProfile, user: JWTData = Depends(AUTH)):
    return await controller.update_profile(user_id=user.id, data=data)


@router.put("/change-password")
async def change_password(data: request.ChangePassword, user: JWTData = Depends(AUTH)):
    return await controller.change_password(user_id=user.id, data=data)


@router.get("/notifications")
async def get_notifications(user: JWTData = Depends(AUTH)):
    return await controller.get_notifications(user_id=user.id)


@router.put("/notifications/{notification_id}")
async def mark_notification_as_read(
    notification_id: int,
    user: JWTData = Depends(AUTH),
):
    return await controller.mark_read(notification_id=notification_id, user_id=user.id)


@router.put("/notifications")
async def mark_all_notifications_as_read(user: JWTData = Depends(AUTH)):
    return await controller.mark_all_read(user_id=user.id)


@router.get("/rentals")
async def get_bookings(user: JWTData = Depends(AUTH)):
    return await controller.get_bookings(user_id=user.id)


@router.get("/rentals/{booking_id}")
async def get_booking(booking_id: int, user: JWTData = Depends(AUTH)):
    return await controller.get_booking(booking_id=booking_id, user_id=user.id)


@router.post("/rentals/cancel")
async def cancel_booking(booking_id: int, user: JWTData = Depends(AUTH)):
    return await controller.cancel_booking(booking_id=booking_id, user_id=user.id)
