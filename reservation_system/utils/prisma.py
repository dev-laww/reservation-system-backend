import asyncio

from prisma import Prisma


prisma = Prisma()


def get_db_session() -> Prisma:
    """
    Get session to database.

    :return: new session.
    """
    if not prisma.is_connected():
        loop = asyncio.get_running_loop()
        loop.run_until_complete(prisma.connect())

    return prisma
