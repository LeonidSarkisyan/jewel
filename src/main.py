import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN
from src.routers import systems, base, chat, weather, gem


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

    dp = Dispatcher()

    routers = [base.router, chat.router, weather.router, gem.router]

    for router in routers:
        dp.include_router(router)

    dp.startup.register(systems.get_start)
    dp.shutdown.register(systems.get_stop)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


asyncio.run(start())
