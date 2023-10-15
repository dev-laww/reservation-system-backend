from fastapi import HTTPException, status

from ..repositories import PropertyRepository
from ..schemas.property import Booking, Property, Review
from ..schemas.request import (
    BookingCreate,
    PropertyCreate,
    PropertyUpdate,
    ReviewCreate,
    ReviewUpdate,
)
from ..schemas.user import Tenant
from ..utils.response import Response


class PropertyController:
    repo = PropertyRepository()

    async def get_property(self, property_id: int):
        """
        Get property by id.

        :param property_id: data id.
        :return: Property.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        property_data = {
            **data.model_dump(),
            "current_occupant": len(data.tenants),
        }

        return Response.ok(
            message="Property retrieved",
            data=Property(**property_data).model_dump(),
        )

    async def get_properties(self):
        """
        Get all properties.

        :return: Properties.
        """
        properties = await self.repo.get_all()

        return Response.ok(
            message="Properties retrieved",
            data=[
                Property(
                    **{
                        **data.model_dump(),
                        "current_occupant": len(data.tenants),
                    }
                ).model_dump()
                for data in properties
            ],
        )

    async def create_property(self, data: PropertyCreate):
        """
        Create property.

        :param data: property data.
        :return: Property.
        """
        data = await self.repo.create(**data.model_dump())

        return Response.ok(
            message="Property created",
            data=Property(**data.model_dump()).model_dump(),
        )

    async def update_property(self, property_id: int, data: PropertyUpdate):
        """
        Update data.

        :param property_id: data id.
        :param data: property data.
        :return: Property.
        """
        parsed = {k: v for k, v in data.model_dump().items() if v}
        data = await self.repo.update(property_id=property_id, **parsed)

        if not data:
            raise Response.not_found(message="Property not found")

        return Response.ok(
            message="Property updated",
            data=Property(**data.model_dump()).model_dump(),
        )

    async def delete_property(self, property_id: int):
        """
        Delete property.

        :param property_id: data id.
        :return: Property.
        """
        data = await self.repo.delete(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        return Response.ok(
            message="Property deleted",
            data=Property(**data.model_dump()).model_dump(),
        )

    async def get_reviews(self, property_id: int):
        """
        Get property reviews.

        :param property_id: data id.
        :return: Property reviews.
        """
        reviews = await self.repo.get_reviews(property_id=property_id)

        return Response.ok(
            message="Property reviews retrieved",
            data=reviews,
        )

    async def add_review(self, property_id: int, user_id: int, data: ReviewCreate):
        """
        Add property review.

        :param property_id: data id.
        :param user_id: user id.
        :param data: review data.
        :return: Property reviews.
        """
        prop = await self.repo.get_by_id(property_id=property_id)

        if not prop:
            raise Response.not_found(message="Property not found")

        review = await self.repo.create_review(
            property_id, user_id=user_id, **data.model_dump()
        )

        return Response.ok(
            message="Property review added",
            data=Review(**review.model_dump()).model_dump(),
        )

    async def update_review(
        self,
        property_id: int,
        review_id: int,
        user_id: int,
        data: ReviewUpdate,
    ):
        """
        Update data review.

        :param property_id: data id.
        :param review_id: review id.
        :param user_id: user id.
        :param data: review data.
        :return: Property reviews.
        """
        prop = await self.repo.get_by_id(property_id=property_id)

        if not prop:
            raise Response.not_found(message="Property not found")

        review = await self.repo.get_review(review_id=review_id)

        if not review or user_id != review.user_id:
            raise Response.not_found(message="Review not found")

        review = await self.repo.update_review(review_id=review_id, **data.model_dump())

        return Response.ok(
            message="Property review updated",
            data=Review(
                **{k: v for k, v in review.model_dump().items() if v is not None}
            ).model_dump(),
        )

    async def delete_review(self, property_id: int, review_id: int, user_id: int):
        """
        Delete data review.

        :param property_id: data id.
        :param review_id: review id.
        :param user_id: user id.
        :return: Property reviews.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        review = await self.repo.get_review(review_id=review_id)

        if not review or user_id != review.user_id:
            raise Response.not_found(message="Review not found")

        return Response.ok(
            message="Property review deleted",
            data=Review(**review.model_dump()).model_dump(),
        )

    async def get_bookings(self, property_id: int):
        """
        Get data bookings.

        :param property_id: data id.
        :return: Property bookings.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        bookings = await self.repo.get_bookings(property_id=property_id)

        return Response.ok(
            message="Property bookings retrieved",
            data=[Booking(**booking.model_dump()).model_dump() for booking in bookings],
        )

    async def book_property(self, property_id: int, user_id: int, data: BookingCreate):
        """
        Book data.

        :param property_id: data id.
        :param user_id: user id.
        :param data: booking data.
        :return: Property bookings.
        """
        prop = await self.repo.get_by_id(property_id=property_id)

        if not prop:
            raise Response.not_found(message="Property not found")

        if data.current_occupant >= data.max_occupancy:
            raise Response.bad_request(message="Property is full")

        booking_check = await self.repo.get_booking(
            user_id=user_id,
            property_id=property_id,
        )

        if booking_check:
            raise Response.bad_request(message="You already have a booking")

        booking = await self.repo.create_booking(
            property_id=property_id, user_id=user_id, **data.model_dump()
        )

        return Response.ok(
            message="Property booked",
            data=Booking(**booking.model_dump()).model_dump(),
        )

    async def get_tenants(self, property_id: int):
        """
        Get data tenants.

        :param property_id: data id.
        :return: Property tenants.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        tenants = await self.repo.get_tenants(property_id=property_id)

        return Response.ok(
            message="Property tenants retrieved",
            data=[Tenant(**tenant.model_dump()).model_dump() for tenant in tenants],
        )

    async def add_tenant(self, property_id: int, user_id: int):
        """
        Add tenant to data.

        :param property_id: data id.
        :param user_id: user id.
        :return: Property tenants.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        tenant_check = await self.repo.get_tenant(user_id=user_id)

        if tenant_check.property_id == property_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a tenant",
            )

        tenant = await self.repo.add_tenant(property_id=property_id, user_id=user_id)

        if not tenant:
            raise Response.bad_request(message="User not found")

        await self.repo.increment_occupants(property_id=property_id)

        return Response.ok(message="Tenant added")

    async def remove_tenant(self, property_id: int, tenant_id: int):
        """
        Remove tenant from data.

        :param property_id: data id.
        :param tenant_id: tenant id.
        :return: Property tenants.
        """

        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        tenant_check = await self.repo.get_tenant(user_id=tenant_id)

        if not tenant_check or (
            tenant_check and tenant_check.property_id != property_id
        ):
            raise Response.bad_request(message="User is not a tenant")

        await self.repo.remove_tenant(property_id=property_id, user_id=tenant_id)
        await self.repo.decrement_occupants(property_id=property_id)

        return Response.ok(
            message="Tenant removed",
            data=None,
        )
