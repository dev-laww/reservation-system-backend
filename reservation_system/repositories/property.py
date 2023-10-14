from prisma import models

from reservation_system.utils.prisma import get_db_session


class PropertyRepository:
    prisma_client = get_db_session()

    async def get_by_id(self, property_id: int) -> models.Property:
        """
        Get property by id.

        :param property_id: property id.
        :return: Property.
        """
        return await self.prisma_client.property.find_unique(
            where={"id": property_id},
            include={
                "images": True,
                "reviews": True,
                "tenants": True
            }
        )

    async def get_by_name(self, name: str) -> models.Property:
        """
        Get property by name.

        :param name: property name.
        :return: Property.
        """
        return await self.prisma_client.property.find_unique(
            where={"name": name},
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def get_all(self) -> list[models.Property]:
        """
        Get all properties.

        :return: list of properties.
        """
        return await self.prisma_client.property.find_many(
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def create(self, **data) -> models.Property:
        """
        Create property.

        :param data: property data.
        :return: Property.
        """
        return await self.prisma_client.property.create(
            data=data,
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def update(self, property_id: int, **kwargs) -> models.Property:
        """
        Update property.

        :param property_id: property id.
        :param kwargs: property data.
        :return: Property.
        """
        return await self.prisma_client.property.update(
            where={"id": property_id},
            data=kwargs,
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def increment_occupants(self, property_id: int):
        """
        Increment property occupants.

        :param property_id: property id.
        :return: Property.
        """
        return await self.prisma_client.property.update(
            where={"id": property_id},
            data={
                "current_occupant": {
                    "increment": 1
                }
            },
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def decrement_occupants(self, property_id: int):
        """
        Decrement property occupants.

        :param property_id: property id.
        :return: Property.
        """
        return await self.prisma_client.property.update(
            where={"id": property_id},
            data={
                "current_occupant": {
                    "decrement": 1
                }
            },
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def delete(self, property_id: int) -> models.Property:
        """
        Delete property.

        :param property_id: property id.
        :return: Property.
        """
        return await self.prisma_client.property.delete(
            where={"id": property_id},
            include={
                "images": True,
                "reviews": True,
                "tenants": True,
            }
        )

    async def add_image(self, property_id: int, url: str) -> models.Property:
        """
        Add property image.

        :param property_id: property id.
        :param url: image url.
        :return: Property.
        """
        return await self.prisma_client.property.update(
            where={"id": property_id},
            data={
                "images": {
                    "create": {
                        "url": url,
                    },
                },
            },
        )

    async def get_reviews(self, property_id: int) -> list[models.Review]:
        """
        Get property reviews.

        :param property_id: property id.
        :return: list of reviews.
        """
        return await self.prisma_client.review.find_many(where={"property_id": property_id})

    async def get_review(self, review_id: int) -> models.Review:
        """
        Get property review.

        :param review_id: review id.
        :return: Review.
        """
        return await self.prisma_client.review.find_first(where={"id": review_id})

    async def create_review(self, property_id: int, **data) -> models.Review:
        """
        Create a property review.

        :param property_id: property id.
        :param data: review data.
        :returns: Review.
        """
        return await self.prisma_client.review.create(
            data={
                "property_id": property_id,
                **data,
            },
        )

    async def update_review(self, review_id: int, **data) -> models.Review:
        """
        Update a property review.

        :param review_id: property id.
        :param data: review data.
        :returns: Review.
        """
        return await self.prisma_client.review.update(
            where={"id": review_id},
            data=data,
        )

    async def delete_review(self, property_id: int) -> models.Review:
        """
        Delete a property review.

        :param property_id: property id.
        :returns: Review.
        """
        return await self.prisma_client.review.delete(where={"property_id": property_id})

    async def get_bookings(self, property_id: int) -> list[models.Booking]:
        """
        Get property bookings.

        :param property_id: property id.
        :return: list of bookings.
        """
        return await self.prisma_client.booking.find_many(where={"property_id": property_id})

    async def create_booking(self, property_id: int, **data) -> models.Booking:
        """
        Create a property booking.

        :param property_id: property id.
        :param data: booking data.
        :returns: Booking.
        """
        return await self.prisma_client.booking.create(
            data={
                "property_id": property_id,
                **data,
            },
        )

    async def get_booking(self, property_id: int, user_id: int) -> models.Booking:
        """
        Get property booking.

        :param property_id: property id.
        :param user_id: user id.
        :return: Booking.
        """

        return await self.prisma_client.booking.find_first(
            where={"property_id": property_id, "user_id": user_id}
        )

    async def get_tenants(self, property_id: int) -> list[models.User]:
        """
        Get property tenants.

        :param property_id: property id.
        :return: list of tenants.
        """
        return await self.prisma_client.user.find_many(where={"property_id": property_id})

    async def add_tenant(self, property_id: int, user_id: int) -> models.User:
        """
        Add tenant to property.

        :param property_id: property id.
        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.user.update(
            where={"id": user_id},
            data={"property_id": property_id},
        )

    async def remove_tenant(self, property_id: int, user_id: int) -> models.User:
        """
        Remove tenant from property.

        :param property_id: property id.
        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.property.update(
            where={"id": property_id},
            data={"tenants": {"disconnect": {"id": user_id}}},
        )

    async def get_tenant(self, user_id: int) -> models.User:
        """
        Get tenant.

        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.user.find_first(where={"id": user_id})
