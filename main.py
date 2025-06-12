import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.database.models import async_main
from app.handlers.__init__ import setup_routers
from app.commands.commands_menu import set_commands


async def main() -> None:
    await async_main() #Создание БД
    #Подключение бота и диспетчера по токену из .env
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    print("bot is working")
    #Подключение роутеров к диспетчеру и вывод базовых команд
    dp.include_routers(setup_routers())
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    #Запуск бота, при остановке вывести сообщение
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot was stopped")
