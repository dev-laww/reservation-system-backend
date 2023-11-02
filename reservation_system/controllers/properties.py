import requests
from fastapi import HTTPException, UploadFile, status

from ..repositories import PropertyRepository, NotificationRepository
from ..schemas.property import Rental, Property, Review
from ..schemas.query_params import PropertyQuery
from ..schemas.request import (
    BookingCreate,
    PropertyCreate,
    PropertyUpdate,
    ReviewCreate,
    ReviewUpdate,
)
from ..schemas.user import Tenant
from ..settings import settings
from ..utils.response import Response


class PropertiesController:
    repo = PropertyRepository()
    notif_repo = NotificationRepository()

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

    async def get_properties(self, filters: PropertyQuery):
        """
        Get all properties.

        :return: Properties.
        """
        properties = await self.repo.get_all(filters)

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
        Get data rentals.

        :param property_id: data id.
        :return: Property rentals.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        rentals = await self.repo.get_bookings(property_id=property_id)

        return Response.ok(
            message="Property rentals retrieved",
            data=[Rental(**rental.model_dump()).model_dump() for rental in rentals],
        )

    async def book_property(self, property_id: int, user_id: int, data: BookingCreate):
        """
        Book data.

        :param property_id: data id.
        :param user_id: user id.
        :param data: rental data.
        :return: Property rentals.
        """
        prop = await self.repo.get_by_id(property_id=property_id)

        if not prop:
            raise Response.not_found(message="Property not found")

        if prop.current_occupant >= prop.max_occupancy:
            raise Response.bad_request(message="Property is full")

        booking_check = await self.repo.get_booking(
            user_id=user_id,
            property_id=property_id,
        )

        if booking_check:
            raise Response.bad_request(message="You already have a rental")

        rental = await self.repo.create_booking(
            property_id=property_id, user_id=user_id, **data.model_dump()
        )

        return Response.ok(
            message="Property booked",
            data=Rental(**rental.model_dump()).model_dump(),
        )

    async def accept_booking(self, booking_id: int):
        """Accept data rental.

        :param booking_id: rental id.
        :return: Property rentals.
        """

        rental = await self.repo.get_booking_by_id(booking_id=booking_id)

        if not rental:
            raise Response.not_found(message="Rental not found")

        await self.repo.delete_booking(booking_id=booking_id)
        await self.repo.add_tenant(
            property_id=rental.property_id, user_id=rental.user_id
        )
        await self.notif_repo.create(
            user_id=rental.user_id,
            message=f"Your rental for {rental.property.name} has been accepted",
            created_by="SYSTEM",
        )

        return Response.ok(message="Rental accepted")

    async def decline_booking(self, booking_id: int):
        """Decline data rental.

        :param booking_id: rental id.
        :return: Property rentals.
        """

        rental = await self.repo.get_booking_by_id(booking_id=booking_id)

        if not rental:
            raise Response.not_found(message="Rental not found")

        await self.repo.delete_booking(booking_id=booking_id)
        await self.notif_repo.create(
            user_id=rental.user_id,
            message=f"Your rental for {rental.property.name} has been declined",
            created_by="SYSTEM",
        )

        return Response.ok(message="Rental declined")

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

        if not tenant_check:
            raise Response.not_found(message="User not found")

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

    async def upload_image(self, property_id: int, image: UploadFile):
        """
        Upload property image.

        :param property_id: data id.
        :param image: image file.
        """

        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        if "image" not in image.headers.get("Content-Type"):
            raise Response.bad_request(message="Invalid image file")

        url = "https://thumbsnap.com/api/upload"
        resp = requests.post(
            url,
            data={"key": settings.thumbsnap_secret},
            files={"media": image.file.read()},
        )

        if resp.status_code != 200:
            raise Response.bad_request(message="Image upload failed")

        image = resp.json()["data"]["thumb"]
        await self.repo.add_image(property_id=property_id, url=image)

        return Response.ok(message="Image uploaded")

    async def remove_image(self, property_id: int, image_id: int):
        """
        Remove property image.

        :param property_id: data id.
        :param image_id: image id.
        """

        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        image = await self.repo.get_image(property_id=property_id, image_id=image_id)

        if not image:
            raise Response.not_found(message="Image not found")

        await self.repo.remove_image(image_id=image_id)

        return Response.ok(message="Image removed")
