import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import asyncpg

from uchidomabot.config import load_config
from uchidomabot.filters.role import RoleFilter, AdminFilter
from uchidomabot.handlers.admin import register_admin
from uchidomabot.handlers.user import register_user
from uchidomabot.middlewares.db import DbMiddleware
from uchidomabot.middlewares.role import RoleMiddleware
from uchidomabot.middlewares.http_client import ClientMiddleware
from cheapshapi.client import CheapShark


logger = logging.getLogger(__name__)


def create_pool(user, password, database, host, echo):
    return asyncpg.create_pool(
        user=user, password=password, database=database, host=host
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.middleware.setup(ClientMiddleware(CheapShark()))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == "__main__":
    cli()
