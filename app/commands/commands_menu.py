from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="запустить бота"
        ),
        BotCommand(
            command="top",
            description="Топ клоунов"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
