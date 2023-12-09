from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Главное меню'
        ),
        BotCommand(
            command='cancel',
            description='Отменить действие'
        )
    ]

    await bot.set_my_commands(commands)
