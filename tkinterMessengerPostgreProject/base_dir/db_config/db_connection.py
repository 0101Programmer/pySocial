from tortoise import Tortoise
from base_dir.config import db_password, db_name


async def tortoise_init():
    await Tortoise.init(db_url=f'asyncpg://postgres:{db_password}@localhost:5432/{db_name}',
                        modules={"app": ["base_dir.db_config.db_models"]})
    await Tortoise.generate_schemas(safe=True)
