from prisma import models

from ..utils.prisma import get_db_session


class PaymentRepository:
    prisma_client = get_db_session()

    async def get_by_id(self, payment_id: int) -> models.Payment:
        """
        Get payment by id.

        :param payment_id: payment id.
        :return: Payment.
        """
        return await self.prisma_client.payment.find_unique(
            where={"id": payment_id},
            include={
                "rental": {
                    "include": {
                        "property": True
                    }
                },
                "user": True
            }
        )

    async def get_all(self) -> list[models.Payment]:
        """
        Get all payments.

        :return: list of payments.
        """
        return await self.prisma_client.payment.find_many(
            include={
                "rental": {
                    "include": {
                        "property": True
                    }
                },
                "user": True
            }
        )

    async def create(self, **data) -> models.Payment:
        """
        Create payment.

        :param data: payment data.
        :return: Payment.
        """
        return await self.prisma_client.payment.create(data=data)

    async def update(self, payment_id: int, **kwargs) -> models.Payment:
        """
        Update payment.

        :param payment_id: payment id.
        :param kwargs: payment data.
        :return: Payment.
        """
        return await self.prisma_client.payment.update(
            where={"id": payment_id},
            data=kwargs,
            include={
                "rental": {
                    "include": {
                        "property": True
                    }
                },
                "user": True
            }
        )

    async def delete(self, payment_id: int) -> models.Payment:
        """
        Delete payment.

        :param payment_id: payment id.
        :return: Payment.
        """
        return await self.prisma_client.payment.delete(where={"id": payment_id})

    async def mark_paid(self, payment_id: int) -> models.Payment:
        """
        Mark payment as paid.

        :param payment_id: payment id.
        :return: Payment.
        """
        return await self.prisma_client.payment.update(
            where={"id": payment_id},
            data={"status": "PAID"},
            include={
                "rental": {
                    "include": {
                        "property": True
                    }
                },
                "user": True
            }
        )

    async def mark_declined(self, payment_id: int) -> models.Payment:
        """
        Mark payment as declined.

        :param payment_id: payment id.
        :return: Payment.
        """
        return await self.prisma_client.payment.update(
            where={"id": payment_id},
            data={"status": "DECLINED"},
            include={
                "rental": {
                    "include": {
                        "property": True
                    }
                },
                "user": True
            }
        )
