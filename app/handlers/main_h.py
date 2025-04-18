from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.database import requests as rq

main_r = Router()
main_r.message.filter(F.chat.type == 'supergroup')


@main_r.message(CommandStart())
async def cmd_start(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, user_name=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    await message.reply("Ебать ты клоун, конечно, но молодец, что воспользовался командой")