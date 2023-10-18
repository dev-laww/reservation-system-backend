import asyncio
import json
import os
from typing import Any, List

import humps
from dotenv import load_dotenv
from prisma import Prisma

load_dotenv()

non_relational_tables = [
    'user'
]


async def assemble_seed_map():
    """
    Assemble seeder map.
    """
    seeders = os.listdir('./seeders')

    prisma = Prisma()

    await prisma.connect()

    seed_map = {}

    # JSON files
    for seeder in seeders:
        if not seeder.endswith('.json'):
            continue

        with open(f'./seeders/{seeder}', 'r') as f:
            data = json.load(f)
            table_name = humps.decamelize(seeder.split('.')[0])

            seed_map[table_name] = {
                'data': data,
                'prisma': getattr(prisma, table_name)
            }

    return seed_map


async def seed(table_data: List[dict], prisma: Any, table_name: str):
    for data in table_data:
        exists = await prisma.find_first(
            where={
                'id': data['id']
            }
        )

        if exists:
            print(f'{table_name} {data["id"]} already exists.')
            continue

        await prisma.create(data=data)

        print(f'Seeded {table_name} {data["id"]}.')


async def main():
    """
    Seed database with initial data.
    """
    seed_map = await assemble_seed_map()

    print('Seeding database...')

    for table_name, table_data in seed_map.items():
        print(f'Seeding {table_name}...')

        if table_name in non_relational_tables:
            await seed(table_data['data'], table_data['prisma'], table_name)

            continue

        await seed(table_data['data'], table_data['prisma'], table_name)

    print('Done.')


if __name__ == "__main__":
    asyncio.run(main())
