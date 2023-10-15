from fastapi import APIRouter, Depends
from reservation_system.controllers.profile import ProfileController
from reservation_system.schemas.token import JWTData
from reservation_system.utils.jwt import AUTH
from reservation_system.web.api.profile import schema

router = APIRouter()
controller = ProfileController()


@router.get("")
async def get_profile(user: JWTData = Depends(AUTH)):
    return await controller.get_profile(user_id=user.id)


@router.put("")
async def update_profile(data: schema.UpdateProfile, user: JWTData = Depends(AUTH)):
    return await controller.update_profile(user_id=user.id, data=data)


@router.put("/change-password")
async def change_password(data: schema.ChangePassword, user: JWTData = Depends(AUTH)):
    return await controller.change_password(user_id=user.id, data=data)


@router.get("/notifications")
async def get_notifications(user: JWTData = Depends(AUTH)):
    return await controller.get_notifications(user_id=user.id)


@router.put("/notifications/{notification_id}")
async def mark_notification_as_read(
    notification_id: int, user: JWTData = Depends(AUTH)
):
    return await controller.mark_read(notification_id=notification_id, user_id=user.id)


@router.put("/notifications")
async def mark_all_notifications_as_read(user: JWTData = Depends(AUTH)):
    return await controller.mark_all_read(user_id=user.id)


@router.get("/bookings")
async def get_bookings(user: JWTData = Depends(AUTH)):
    return await controller.get_bookings(user_id=user.id)


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: int, user: JWTData = Depends(AUTH)):
    return await controller.get_booking(booking_id=booking_id, user_id=user.id)


@router.post("/bookings/cancel")
async def cancel_booking(booking_id: int, user: JWTData = Depends(AUTH)):
    return await controller.cancel_booking(booking_id=booking_id, user_id=user.id)
