import asyncio

from prisma import Prisma

prisma = Prisma()
asyncio.create_task(prisma.connect())


def get_db_session() -> Prisma:
    """
    Get session to database.

    :return: new session.
    """
    return prisma
