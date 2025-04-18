import random
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, FSInputFile


from app.database import requests as rq
from app.database import models as md


unexpected_event_r = Router()
unexpected_event_r.message.filter(F.chat.type == 'supergroup')


@unexpected_event_r.message(F.text.lower().contains("🤡") | F.text.lower().contains("клоун"))
async def clown(message: Message) -> Any:
    addClownizm = random.randint(1, 10)
    await rq.set_user(user_id=message.from_user.id, user_name=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    user = await rq.get_user(user_id=message.from_user.id)
    user.clownizm += addClownizm
    async with md.async_session() as session:
        await session.merge(user)
    await message.reply(f"Ебать ты клоун, конечно\n+{addClownizm} к клоунизму")

