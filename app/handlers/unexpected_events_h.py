import random
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from app.database import requests as rq
from app.database import models as md

#Создаём роутер и заставляем обрабатывать его сообщения в групповых чатах
unexpected_event_r = Router()
unexpected_event_r.message.filter(F.chat.type == 'supergroup')

#Если в сообщение есть Клоун, то...
@unexpected_event_r.message(F.text.lower().contains("🤡") | F.text.lower().contains("клоун"))
async def clown(message: Message) -> Any:
    addClownizm = random.randint(1, 10) #Выбор рандомного числа клоунизма
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    user = await rq.get_obj(user_id=message.from_user.id, obj_class=md.User) #Достаём пользователя
    user.clownizm += addClownizm #Добавляем клоунизма, который мы сгенерировали к клоунизму пользователя
    async with md.async_session() as session:
        await session.merge(user) #Записать изменения
        await session.commit() #Сохранить изменения в БД
    await message.reply(f"Ебать ты клоун, конечно\n+{addClownizm} к клоунизму") #Вывести сообщение

#Если в сообщении есть Сосал, то...
@unexpected_event_r.message(F.text.lower().contains("сосал"))
async def sucked(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    user = await rq.get_obj(user_id=message.from_user.id, obj_class=md.User) #Достаём пользователя по User
    wasAnything = await rq.get_obj(user_id=message.from_user.id, obj_class=md.WasAnything) #Достаём пользователя по WasAnything
    if wasAnything.wasSucked == False: #Если этого не происходило ранее
        user.clownizm += 1 #Добовляем клоунизм
        wasAnything.wasSucked = True #Помечаем произошедшим (чтобы событие не повторилось второй раз для того же пользователя)
        async with md.async_session() as session:
            await session.merge(user) #Записать изменения User
            await session.merge(wasAnything) #Записать изменения WasAnything
            await session.commit() #Сохранить изменения в БД
        await message.reply("Да, я сосал") #Вывести сообщение

