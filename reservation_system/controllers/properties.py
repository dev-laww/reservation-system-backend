from fastapi import HTTPException, status

from reservation_system.repositories.property import PropertyRepository
from reservation_system.utils.responses import SuccessResponse, Error
from reservation_system.schemas.property import Property, Review, Booking
from reservation_system.schemas.user import Tenant
from reservation_system.schemas.query_params import PropertyQuery
from reservation_system.web.api.property.schema import (
    PropertyCreate,
    PropertyUpdate,
    ReviewCreate,
    ReviewUpdate,
    BookingCreate,
)


class PropertyController:
    repo = PropertyRepository()

    async def get_property(self, property_id: int):
        """
        Get property by id.

        :param property_id: property id.
        :return: Property.
        """
        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        property_data = {
            **property.model_dump(),
            "current_occupant": len(property.tenants),
        }
        print(property_data)
        return SuccessResponse(
            message="Property retrieved", data=Property(**property_data).model_dump()
        )

    async def get_properties(self, filters: PropertyQuery):
        """
        Get all properties.

        :return: Properties.
        """

        properties = await self.repo.get_all(filters)

        return SuccessResponse(
            message="Properties retrieved",
            data=[
                Property(
                    **{
                        **property.model_dump(),
                        "current_occupant": len(property.tenants),
                    }
                ).model_dump()
                for property in properties
            ],
        )

    async def create_property(self, data: PropertyCreate):
        """
        Create property.

        :param property: property data.
        :return: Property.
        """

        property = await self.repo.create(**data.model_dump())

        return SuccessResponse(
            message="Property created",
            data=Property(**property.model_dump()).model_dump(),
        )

    async def update_property(self, property_id: int, data: PropertyUpdate):
        """
        Update property.

        :param property_id: property id.
        :param data: property data.
        :return: Property.
        """

        parsed = {k: v for k, v in data.model_dump().items() if v}
        property = await self.repo.update(property_id=property_id, **parsed)

        if not property:
            raise Error.NOT_FOUND

        return SuccessResponse(
            message="Property updated",
            data=Property(**property.model_dump()).model_dump(),
        )

    async def delete_property(self, property_id: int):
        """
        Delete property.

        :param property_id: property id.
        :return: Property.
        """

        property = await self.repo.delete(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        return SuccessResponse(
            message="Property deleted",
            data=Property(**property.model_dump()).model_dump(),
        )

    async def get_reviews(self, property_id: int):
        """
        Get property reviews.

        :param property_id: property id.
        :return: Property reviews.
        """

        property = await self.repo.get_reviews(property_id=property_id)

        return SuccessResponse(message="Property reviews retrieved", data=property)

    async def add_review(self, property_id: int, user_id: int, data: ReviewCreate):
        """
        Add property review.

        :param property_id: property id.
        :param user_id: user id.
        :param review: review data.
        :return: Property reviews.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        review = await self.repo.create_review(
            property_id, user_id=user_id, **data.model_dump()
        )

        return SuccessResponse(
            message="Property review added",
            data=Review(**review.model_dump()).model_dump(),
        )

    async def update_review(
        self, property_id: int, review_id: int, user_id: int, data: ReviewUpdate
    ):
        """
        Update property review.

        :param property_id: property id.
        :param review_id: review id.
        :param data: review data.
        :return: Property reviews.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        review = await self.repo.update_review(review_id=review_id, **data.model_dump())

        if not review or user_id != review.user_id:
            raise Error.NOT_FOUND

        return SuccessResponse(
            message="Property review updated",
            data=Review(
                **{k: v for k, v in review.model_dump().items() if v is not None}
            ).model_dump(),
        )

    async def delete_review(self, property_id: int, review_id: int, user_id: int):
        """
        Delete property review.

        :param property_id: property id.
        :param review_id: review id.
        :param user_id: user id.
        :return: Property reviews.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        review = await self.repo.get_review(review_id=review_id)

        if not review or user_id != review.user_id:
            raise Error.NOT_FOUND

        return SuccessResponse(
            message="Property review deleted",
            data=Review(**review.model_dump()).model_dump(),
        )

    async def get_bookings(self, property_id: int):
        """
        Get property bookings.

        :param property_id: property id.
        :return: Property bookings.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        bookings = await self.repo.get_bookings(property_id=property_id)

        return SuccessResponse(
            message="Property bookings retrieved",
            data=[Booking(**booking.model_dump()).model_dump() for booking in bookings],
        )

    async def book_property(self, property_id: int, user_id: int, data: BookingCreate):
        """
        Book property.

        :param property_id: property id.
        :return: Property bookings.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        if property.current_occupant >= property.max_occupancy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Property is full"
            )

        booking_check = await self.repo.get_booking(
            user_id=user_id, property_id=property_id
        )

        if booking_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a booking",
            )

        booking = await self.repo.create_booking(
            property_id=property_id, user_id=user_id, **data.model_dump()
        )

        return SuccessResponse(
            message="Property booked", data=Booking(**booking.model_dump()).model_dump()
        )

    async def get_tenants(self, property_id: int):
        """
        Get property tenants.

        :param property_id: property id.
        :return: Property tenants.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        tenants = await self.repo.get_tenants(property_id=property_id)

        return SuccessResponse(
            message="Property tenants retrieved",
            data=[Tenant(**tenant.model_dump()).model_dump() for tenant in tenants],
        )

    async def add_tenant(self, property_id: int, user_id: int):
        """
        Add tenant to property.

        :param property_id: property id.
        :param user_id: user id.
        :return: Property tenants.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        tenant_check = await self.repo.get_tenant(user_id=user_id)

        if tenant_check.property_id == property_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a tenant",
            )

        tenant = await self.repo.add_tenant(property_id=property_id, user_id=user_id)

        if not tenant:
            raise Error.NOT_FOUND

        await self.repo.increment_occupants(property_id=property_id)

        return SuccessResponse(
            message="Tenant added", data=Tenant(**tenant.model_dump()).model_dump()
        )

    async def remove_tenant(self, property_id: int, tenant_id: int):
        """
        Remove tenant from property.

        :param property_id: property id.
        :param tenant_id: tenant id.
        :return: Property tenants.
        """

        property = await self.repo.get_by_id(property_id=property_id)

        if not property:
            raise Error.NOT_FOUND

        tenant_check = await self.repo.get_tenant(user_id=tenant_id)

        if not tenant_check or (
            tenant_check and tenant_check.property_id != property_id
        ):
            raise Error.NOT_FOUND

        await self.repo.remove_tenant(property_id=property_id, user_id=tenant_id)
        await self.repo.decrement_occupants(property_id=property_id)

        return SuccessResponse(message="Tenant removed", data=None)
