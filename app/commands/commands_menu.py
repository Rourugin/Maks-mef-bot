from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    #Список команд
    commands = [
        BotCommand(
            command="start", #Команда (через '/' в боте)
            description="Запустить бота" #Описание
        ),
        BotCommand(
            command="top",
            description="Топ клоунов"
        ),
        BotCommand(
            command="info",
            description="Информация об участнике"
        ),
        BotCommand(
            command="tozero",
            description="Обнулиться"
        ),
        BotCommand(
            command="casino",
            description="Казино"
        )
    ]
    #Создать список команд рядом/над клавиатурой (автоматически определяется тг)
    await bot.set_my_commands(commands, BotCommandScopeDefault())