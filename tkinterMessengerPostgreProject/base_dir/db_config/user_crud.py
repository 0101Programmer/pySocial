import asyncio
from tortoise import Tortoise
from tortoise.connection import connections

from base_dir.config import db_password, db_name
from base_dir.db_config.db_models import User

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def create_user():
    await User.create(email="sm@mail.ru", password="1", name="tester", birthdate="2000-12-12",
                      session_data={"status": "inactive", "system_info": None}, )


async def get_users():
    users = await User.all().order_by("-created_at")
    print(users)


async def delete_user_by_id():
    user = await User.get(id=2)
    await user.delete()


async def delete_all_users():
    await User.all().delete()


async def update_user_by_id():
    user = await User.get(id=5)
    user.friends["6"] = {
        "his_email": "m@mail.ru",
        "my_confirmation": True,
        "his_confirmation": True
    }
    await user.save()


async def tortoise_init():
    await Tortoise.init(db_url=f'asyncpg://postgres:{db_password}@localhost:5432/{db_name}',
                        modules={"app": ["base_dir.db_config.db_models"]})
    await Tortoise.generate_schemas(safe=True)

    await create_user()


if __name__ == '__main__':
    try:
        loop.run_until_complete(tortoise_init())
    finally:
        loop.run_until_complete(connections.close_all())
        loop.close()
