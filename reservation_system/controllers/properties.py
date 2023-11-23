import requests
from fastapi import HTTPException, UploadFile, status

from ..repositories import (PropertyRepository, NotificationRepository, UserRepository,
                            PaymentRepository)
from ..schemas.property import Rental, Property, Review
from ..schemas.query_params import PropertyQuery
from ..schemas.request import (
    RentalCreate,
    PropertyCreate,
    PropertyUpdate,
    ReviewCreate,
    ReviewUpdate,
)
from ..schemas.user import Tenant
from ..settings import settings
from ..utils.response import Response


class PropertiesController:
    user_repo = UserRepository()
    repo = PropertyRepository()
    notif_repo = NotificationRepository()
    payment_repo = PaymentRepository()

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
            "occupied": bool(data.tenant_property),
            "tenant": data.tenant_property.user.model_dump() if data.tenant_property else None,
            "ratings": await self.get_ratings(property_id=property_id)
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
        await self.get_ratings(property_id=1)
        properties = await self.repo.get_all(filters)

        return Response.ok(
            message="Properties retrieved",
            data=[
                Property(
                    **{
                        **data.model_dump(),
                        "occupied": bool(data.tenant_property),
                        "tenant": data.tenant_property.user.model_dump() if data.tenant_property else None,
                        "ratings": await self.get_ratings(property_id=data.id),
                    }
                ).model_dump()
                for data in properties
            ],
        )

    async def create_property(self, data_in: PropertyCreate):
        """
        Create property.

        :param data: property data.
        :return: Property.
        """

        data = await self.repo.create(**data_in.model_dump())

        return Response.ok(
            message="Property created",
            data=Property(**{
                **data.model_dump(),
                "tenant": data.tenant_property.user.model_dump() if data.tenant_property else None,
                "ratings": await self.get_ratings(property_id=data.id),
            }).model_dump(),
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
            data=Property(**{
                **data.model_dump(),
                "tenant": data.tenant_property.user.model_dump() if data.tenant_property else None,
                "ratings": await self.get_ratings(property_id=data.id),
            }).model_dump(),
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
            data=Property(**{
                **data.model_dump(),
                "tenant": data.tenant_property.user.model_dump() if data.tenant_property else None,
                "ratings": await self.get_ratings(property_id=data.id),
            }).model_dump(),
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

    async def get_rentals(self, property_id: int):
        """
        Get data rentals.

        :param property_id: data id.
        :return: Property rentals.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        rentals = await self.repo.get_rentals(property_id=property_id)

        return Response.ok(
            message="Property rentals retrieved",
            data=[Rental(**rental.model_dump()).model_dump() for rental in rentals],
        )

    async def book_property(self, property_id: int, user_id: int, data: RentalCreate):
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

        if prop.tenant_property:
            raise Response.bad_request(message="Property is taken")

        rental_check = await self.repo.get_rental(
            user_id=user_id,
            property_id=property_id,
        )

        if rental_check:
            raise Response.bad_request(message="You already have a rental")

        rental = await self.repo.create_rental(
            property_id=property_id,
            user_id=user_id,
            start_date=data.start_date,
            end_date=data.end_date,
        )

        payment = await self.payment_repo.create(
            user_id=user_id,
            rental_id=rental.id,
            amount=data.amount,
        )
        payment = payment.model_dump()
        rental = rental.model_dump()
        rental["payment"] = payment

        return Response.ok(
            message="Property booked",
            data=Rental(**rental).model_dump(),
        )

    async def accept_rental(self, rental_id: int):
        """Accept data rental.

        :param rental_id: rental id.
        :return: Property rentals.
        """

        rental = await self.repo.get_rental_by_id(rental_id=rental_id)

        if not rental:
            raise Response.not_found(message="Rental not found")

        await self.repo.accept_rental(rental_id=rental_id)

        if not rental.property.tenant_property:
            await self.repo.add_tenant(
                property_id=rental.property_id, user_id=rental.user_id
            )
            await self.notif_repo.create(
                user_id=rental.user_id,
                message=f"Your rental for {rental.property.name} has been accepted",
                created_by="SYSTEM",
            )

        return Response.ok(message="Rental accepted")

    async def decline_rental(self, rental_id: int):
        """Decline data rental.

        :param rental_id: rental id.
        :return: Property rentals.
        """

        rental = await self.repo.get_rental_by_id(rental_id=rental_id)

        if not rental:
            raise Response.not_found(message="Rental not found")

        await self.repo.decline_rental(rental_id=rental_id)
        await self.notif_repo.create(
            user_id=rental.user_id,
            message=f"Your rental for {rental.property.name} has been declined",
            created_by="SYSTEM",
        )

        return Response.ok(message="Rental declined")

    async def get_tenants(self, property_id: int):
        """
        Get data tenant.

        :param property_id: data id.
        :return: Property tenants.
        """
        data = await self.repo.get_by_id(property_id=property_id)

        if not data:
            raise Response.not_found(message="Property not found")

        if not data.tenant_property:
            raise Response.not_found(message="Property has no tenants")

        return Response.ok(
            message="Property tenants retrieved",
            data=Tenant(**{
                **data.tenant_property.user.model_dump(),
                "property": data.model_dump()
            }).model_dump()
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

        user = await self.user_repo.get_by_id(user_id=user_id)

        if not user:
            raise Response.bad_request(message="User not found")

        if (
            data.tenant_property or user.tenant_property
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property already taken or User is already in a property.",
            )

        await self.repo.add_tenant(property_id=property_id, user_id=user_id)
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

        tenant_check = await self.repo.get_tenant(property_id=property_id)

        if not tenant_check or tenant_check.user.id != tenant_id:
            raise Response.bad_request(message="User is not a tenant of this property")

        await self.repo.remove_tenant(property_id=property_id, user_id=tenant_id)

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

    async def get_ratings(self, property_id: int) -> int:
        return await self.repo.get_ratings(property_id=property_id)
