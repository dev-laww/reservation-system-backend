import asyncio

from prisma import Prisma


prisma = Prisma()


def get_db_session() -> Prisma:
    """
    Get session to database.

    :return: new session.
    """
    if not prisma.is_connected():
        asyncio.create_task(prisma.connect())

    return prisma
