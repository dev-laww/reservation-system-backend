from prisma import models

from ..schemas.query_params import PropertyQuery
from ..utils.prisma import get_db_session


class PropertyRepository:
    prisma_client = get_db_session()

    async def get_by_id(self, property_id: int) -> models.Property:
        """
        Get property by id.

        :param property_id: property id.
        :return: Property.
        """
        return await self.prisma_client.property.find_first(
            where={"id": property_id},
            include={
                "images": True,
                "reviews": {
                    "include": {"user": True}
                },
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
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
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
        )

    async def get_all(self, filters: PropertyQuery) -> list[models.Property]:
        """
        Get all properties.

        :return: list of properties.
        """

        order = None
        where = {}

        if filters.sort and filters.order:
            order = {filters.sort: filters.order}

        if filters.keyword:
            where["name"] = {"contains": filters.keyword}

        if filters.type and filters.type in (
            "one_bedroom",
            "two_bedroom",
            "studio",
            "house",
        ):
            where["type"] = filters.type

        if filters.min_price or filters.max_price or filters.price:
            where["price"] = {}

            if filters.min_price:
                where["price"]["gte"] = filters.min_price

            if filters.max_price:
                where["price"]["lte"] = filters.max_price

            if filters.price:
                where["price"] = filters.price

        if filters.sort and filters.order:
            if filters.sort in (
                "price",
                "created_at",
                "updated_at",
            ):
                order = {filters.sort: filters.order}

        return await self.prisma_client.property.find_many(
            take=filters.limit,
            skip=filters.offset,
            where=where,
            order=order,
            include={
                "images": True,
                "reviews": True,
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
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
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
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
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
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
                "tenant_property": {
                    "include": {
                        "user": True
                    }
                }
            },
        )

    async def get_image(self, property_id: int, image_id: int) -> models.Image:
        """
        Get property image.

        :param property_id: property id.
        :param image_id: image id.
        """
        return await self.prisma_client.image.find_first(
            where={
                "AND": [
                    {"property_id": property_id},
                    {"id": image_id},
                ],
            },
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

    async def remove_image(self, image_id: int) -> models.Property:
        """
        Remove property image.

        :param image_id: image id.
        :return: Property.
        """
        return await self.prisma_client.image.delete(where={"id": image_id})

    async def get_reviews(self, property_id: int) -> list[models.Review]:
        """
        Get property reviews.

        :param property_id: property id.
        :return: list of reviews.
        """
        return await self.prisma_client.review.find_many(
            where={"property_id": property_id},
            include={
                "user": True,
            },
        )

    async def get_review(self, review_id: int) -> models.Review:
        """
        Get property review.

        :param review_id: review id.
        :return: Review.
        """
        return await self.prisma_client.review.find_first(
            where={"id": review_id},
            include={
                "user": True,
            },
        )

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
        return await self.prisma_client.review.delete(
            where={"property_id": property_id}
        )

    async def get_rentals(self, property_id: int) -> list[models.Rental]:
        """
        Get property rentals.

        :param property_id: property id.
        :return: list of rentals.
        """
        return await self.prisma_client.rental.find_many(
            where={"property_id": property_id},
            include={
                "payment": True,
                "user": True,
                "property": True,
            }
        )

    async def create_rental(self, property_id: int, **data) -> models.Rental:
        """
        Create a property rental.

        :param property_id: property id.
        :param data: rental data.
        :returns: Rental.
        """
        return await self.prisma_client.rental.create(
            data={
                "property_id": property_id,
                **data,
            },
        )

    async def get_rental(self, property_id: int, user_id: int) -> models.Rental:
        """
        Get property rental.

        :param property_id: property id.
        :param user_id: user id.
        :return: Rental.
        """

        return await self.prisma_client.rental.find_first(
            where={
                "property_id": property_id,
                "user_id": user_id,
            },
            include={
                "property": True,
                "user": True,
                "payment": True,
            },
        )

    async def get_rental_by_id(self, rental_id: int) -> models.Rental:
        """
        Get property rental.

        :param property_id: property id.
        :param user_id: user id.
        :return: Rental.
        """

        return await self.prisma_client.rental.find_first(
            where={"id": rental_id},
            include={
                "property": True,
                "user": True,
                "payment": True,
            },
        )

    async def delete_rental(self, rental_id: int) -> models.Rental:
        """
        Delete a property rental.

        :param rental_id: rental id.
        :returns: Rental.
        """
        return await self.prisma_client.rental.delete(where={"id": rental_id})

    async def add_tenant(self, property_id: int, user_id: int) -> models.User:
        """
        Add tenant to property.

        :param property_id: property id.
        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.tenantproperty.create(
            data={
                "property_id": property_id,
                "user_id": user_id,
            }
        )

    async def remove_tenant(self, property_id: int, user_id: int) -> models.TenantProperty:
        """
        Remove tenant from property.

        :param property_id: property id.
        :param user_id: user id.
        :return: User.
        """
        return await self.prisma_client.tenantproperty.delete(
            where={
                "property_id": property_id,
            }
        )

    async def get_tenant(self, property_id: int) -> models.TenantProperty:
        """
        Get tenant.

        :param user_id: user id.
        :return: User.
        """
        data = await self.prisma_client.tenantproperty.find_first(
            where={"property_id": property_id},
            include={"user": {"include": {"tenant_property": {"include": {"property": True}}}}},
        )

        return data
