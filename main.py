import os
import asyncio
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.database.models import async_main
from app.handlers.__init__ import setup_routers
from app.commands.commands_menu import set_commands


app = Flask(__name__)

#Создание эндпоинта для проверки работы сервера
@app.route('/ping')
def ping():
    return "pong", 200

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
        Thread(target=asyncio.run(main())).start()  # Запускаем бота в фоне
        app.run(host='0.0.0.0', port=8080)  # Запускаем веб-сервер
    except KeyboardInterrupt:
        print("bot was stopped")
