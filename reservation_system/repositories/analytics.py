from typing import Any
from datetime import datetime

from ..utils.prisma import get_db_session
from ..utils.response import Response


class AnalyticsRepository:
    prisma_client = get_db_session()

    async def get_all_payments(self, year: int, month: int) -> Any:
        """
        Get all analytics.

        :return: list of analytics.
        """
        where = {"status": "paid"}
        ret = {}

        if month not in range(1, 13):
            raise Response.bad_request(f"Invalid month => {month} [required: 1-12]")

        month_start = datetime(year, month, 1)
        month_end = datetime(year, month + 1, 1)

        where["created_at"] = {
            "gte": month_start,
            "lt": month_end,
        }

        for prop in await self.prisma_client.property.find_many():
            ret[prop.name] = 0

        payments = await self.prisma_client.payment.find_many(
            where=where,
            include={
                "booking": {
                    "include": {
                        "property": True,
                    }
                },
            }
        )

        for payment in payments:
            ret[payment.booking.property.name] += payment.amount

        return Response.ok(
            "Successfully retrieved analytics.",
            data=ret,
        )
