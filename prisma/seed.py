import asyncio
import json
import os
from typing import Any, List

import humps
from dotenv import load_dotenv
from prisma import Prisma

load_dotenv()

seeding_order = [
    'property',
    'user',
    'image',
    'notification',
    'rental',
    'payment',
    'review'
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

    for key in seeding_order:
        print(f'Seeding {key}...')
        if key not in seed_map:
            continue

        await seed(
            table_data=seed_map[key]['data'],
            prisma=seed_map[key]['prisma'],
            table_name=key
        )

    print('Done.')


if __name__ == "__main__":
    asyncio.run(main())
