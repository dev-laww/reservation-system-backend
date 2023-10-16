from fastapi import APIRouter, Depends

from ....controllers import PaymentsController
from ....utils.jwt import ADMIN_AUTH

router = APIRouter(dependencies=[Depends(ADMIN_AUTH)])
controller = PaymentsController()


@router.get("")
async def get_all_payments():
    return await controller.get_all_payments()


@router.get("/{payment_id}")
async def get_payment(payment_id: int):
    return await controller.get_payment(payment_id=payment_id)


@router.post("/{payment_id}/paid")
async def mark_as_paid(payment_id: int):
    return await controller.mark_as_paid(payment_id=payment_id)


@router.post("/{payment_id}/declined")
async def mark_as_declined(payment_id: int):
    return await controller.mark_as_declined(payment_id=payment_id)


@router.delete("/{payment_id}")
async def delete(payment_id: int):
    return await controller.delete(payment_id=payment_id)
