from fastapi import APIRouter, Depends

from ....controllers import PropertiesController
from ....schemas.query_params import PropertyQuery
from ....schemas.request import (
    BookingCreate,
    PropertyCreate,
    PropertyUpdate,
    ReviewCreate,
    ReviewUpdate,
)
from ....utils.jwt import ADMIN_AUTH, AUTH

router = APIRouter()
controller = PropertiesController()


@router.get("")
async def get_properties(filters: PropertyQuery = Depends()):
    return await controller.get_properties(filters=filters)


@router.get("/{property_id}")
async def get_property(property_id: int):
    return await controller.get_property(property_id=property_id)


@router.post("", dependencies=[Depends(ADMIN_AUTH)])
async def create_property(data: PropertyCreate):
    return await controller.create_property(data=data)


@router.put("/{property_id}", dependencies=[Depends(ADMIN_AUTH)])
async def update_property(property_id: int, data: PropertyUpdate):
    return await controller.update_property(property_id=property_id, data=data)


@router.delete("/{property_id}", dependencies=[Depends(ADMIN_AUTH)])
async def delete_property(property_id: int):
    return await controller.delete_property(property_id=property_id)


@router.get("/{property_id}/reviews")
async def get_reviews(property_id: int):
    return await controller.get_reviews(property_id=property_id)


@router.post("/{property_id}/reviews")
async def create_review(property_id: int, data: ReviewCreate, user=Depends(AUTH)):
    return await controller.add_review(
        property_id=property_id,
        user_id=user.id,
        data=data,
    )


@router.put("/{property_id}/reviews/{review_id}")
async def update_review(
    property_id: int,
    review_id: int,
    data: ReviewUpdate,
    user=Depends(AUTH),
):
    return await controller.update_review(
        property_id=property_id,
        review_id=review_id,
        user_id=user.id,
        data=data,
    )


@router.get("/{property_id}/bookings")
async def get_bookings(property_id: int):
    return await controller.get_bookings(property_id=property_id)


@router.post("/{property_id}/bookings")
async def create_booking(property_id: int, data: BookingCreate, user=Depends(AUTH)):
    return await controller.book_property(
        property_id=property_id,
        user_id=user.id,
        data=data,
    )


@router.get("/{property_id}/tenants")
async def get_tenants(property_id: int):
    return await controller.get_tenants(property_id=property_id)


@router.post("/{property_id}/tenants", dependencies=[Depends(ADMIN_AUTH)])
async def add_tenant(property_id: int, user_id: int):
    return await controller.add_tenant(property_id=property_id, user_id=user_id)


@router.delete("/{property_id}/tenants/{tenant_id}", dependencies=[Depends(ADMIN_AUTH)])
async def remove_tenant(property_id: int, tenant_id: int):
    return await controller.remove_tenant(property_id=property_id, tenant_id=tenant_id)
