from prisma import Prisma

prisma = Prisma()


async def get_db_session() -> Prisma:
    """
    Get session to database.

    :return: new session.
    """
    if not prisma.is_connected():
        await prisma.connect()

    return prisma
