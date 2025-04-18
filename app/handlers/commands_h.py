from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.database import requests as rq


commands_r = Router()
commands_r.message.filter(F.chat.type == 'supergroup')


@commands_r.message(Command(commands=['top']))
async def top(message: Message) -> Any:
    users_amount = await rq.count_users()
    users = await rq.get_all_users()
    text = "🤡Эй, вот же они, Главные клоуны чата. Да что там клоуны, это уже целый блядский цирк:\n\n"
    for i in range(0, users_amount):
        if users[i]['user_id'] == message.from_user.id:
            user_place = i+1
    if users_amount > 10:
        users_amount = 10
    for i in range(0, users_amount):
        text += str(i+1)
        text += ". "
        text += users[i]['user_first_name']
        if (users[i]['user_last_name'] != None):
            text += " "
            text += users[i]['user_last_name']
        text += " - "
        text += str(users[i]['clownizm'])
        text += "\n"
    text += "\nА вот и твоё место у параши:\nТы - №"
    text += str(user_place)
    await message.reply(text)


@commands_r.message(Command(commands=['idea']))
async def idea(message: Message):
    await message.forward(chat_id=5604550432)
    await message.answer("Не мог получше что-то придумать, лол?🤡 Ладно, ща с максом поржём над этим (и над тобой)")