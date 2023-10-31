from ..repositories import PaymentRepository, NotificationRepository

from ..utils.response import Response


class PaymentsController:
    def __init__(self):
        self.__repo = PaymentRepository()
        self.__notification_repo = NotificationRepository()

    async def get_all_payments(self):
        payments = await self.__repo.get_all()

        return Response.ok(message="Successfully retrieved payments.", data=payments)

    async def get_payment(self, payment_id: int):
        payment = await self.__repo.get_by_id(payment_id=payment_id)

        if not payment:
            return Response.not_found(message="Payment not found.")

        return Response.ok(message="Successfully retrieved payment.", data=payment)

    async def mark_as_paid(self, payment_id: int):
        payment = await self.__repo.get_by_id(payment_id=payment_id)

        if not payment:
            return Response.not_found(message="Payment not found.")

        await self.__repo.update(payment_id=payment_id, status="paid")
        await self.__notification_repo.create(
            message=f"Payment for {payment.booking.property.name} was marked as paid.",
            user_id=payment.booking.user_id,
            created_by="SYSTEM"
        )
        return Response.ok(message="Successfully marked payment as paid.")

    async def mark_as_declined(self, payment_id: int):
        payment = await self.__repo.get_by_id(payment_id=payment_id)

        if not payment:
            return Response.not_found(message="Payment not found.")

        await self.__repo.update(payment_id=payment_id, status="declined")
        await self.__notification_repo.create(
            message=f"Payment for {payment.booking.property.name} was declined.",
            user_id=payment.booking.user_id,
            created_by="SYSTEM"
        )
        return Response.ok(message="Successfully marked payment as declined.")

    async def delete(self, payment_id: int):
        payment = await self.__repo.get_by_id(payment_id=payment_id)

        if not payment:
            return Response.not_found(message="Payment not found.")

        await self.__repo.delete(payment_id=payment_id)

        return Response.ok(message="Successfully deleted payment.")
