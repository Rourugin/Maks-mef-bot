import os
from typing import Any
from aiogram import Router, F
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.filters import Command

from app.database import models as md
from app.database import requests as rq

#Создаём роутер и заставляем обрабатывать его сообщения в групповых чатах
commands_r = Router()
commands_r.message.filter(F.chat.type == 'supergroup')

#Выводим топ пользователей
@commands_r.message(Command(commands=['top']))
async def top(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    users_amount = await rq.count_users() #Число пользователей
    users = await rq.get_all_users() #Все пользователи
    text = "🤡Эй, вот же они, Главные клоуны чата. Да что там клоуны, это уже целый блядский цирк:\n\n"
    #Находим место пользователя в топе
    for i in range(0, users_amount):
        if users[i]['user_id'] == message.from_user.id:
            user_place = i+1
    #Если число пользователей больше 10, то равняем его 10
    if users_amount > 10:
        users_amount = 10
    #Выводим топ 10 (или меньше, если число пользователей меньше)
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
    #Выводим место польщователя в топе
    text += "\nА вот и твоё место у параши:\nТы - №"
    text += str(user_place)
    #Отправляем сообщение
    await message.reply(text)

#Выводим инвормацию о пользователе
@commands_r.message(Command(commands=['info']))
async def info(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    reply = message.reply_to_message #Пытаемся найти того, на чьё сообщение ответили
    if not reply: #Если не ответ на сообщение, то берём отправителя
        user = await rq.get_obj(user_id=message.from_user.id, obj_class=md.User)
    else: #Если ответ насообщение, то берём того, на чьё сообщение ответили
        await rq.set_user(user_id=reply.from_user.id, first_name=reply.from_user.first_name, last_name=reply.from_user.last_name)
        user = await rq.get_obj(user_id=reply.from_user.id, obj_class=md.User)
    #Выводим всю информацию
    text = "Имя: "
    text += user.user_first_name
    text += "\nПо масти: "
    if user.lear == 0:
        text += "лох червивый"
    elif user.lear == 1:
        text += "бебешкин"
    elif user.lear == 2:
        text += "генеорал сасной армии"
    elif user.lear == 3:
        text += "сапёр\n"
    elif user.lear == 4:
        text += "азартный педик"
    text += "\nОтчимов: "
    if user.stepfathers == 0:
        text += "0 😭"
    elif user.stepfathers > 0:
        text += str(user.stepfathers)
    text += "\nУровень клоунизма: "
    text += str(user.clownizm)
    text += "\nПокорный пёсик: "
    if user.pet == 0:
        text +="У тебя его нет:("
    elif user.pet != 0:
        pet = await rq.get_user(user_id=user.pet)
        text += str(pet.user_first_name)
    await message.reply(text=text) #Отправляем сообщение

#Обнуление всего
@commands_r.message(Command(commands=['tozero']))
async def toZero(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    #Достаём всю информацию о пользователе
    user = await rq.get_obj(user_id=message.from_user.id, obj_class=md.User)
    user_was_anything = await rq.get_obj(user_id=message.from_user.id, obj_class=md.WasAnything)
    user_achievements = await rq.get_obj(user_id=message.from_user.id, obj_class=md.Achievements)
    #обнуляем всю информацию о пользователе (кроме айди и имён)
    user.clownizm = 0
    user.lear = 0
    user.stepfathers = 0
    user.sapper_words = 0
    user_was_anything.isHerpes = False
    user_was_anything.wasJewish = False
    user_was_anything.wasFDC = False
    user_was_anything.wasNu = False
    user_was_anything.wasGandalf = False
    user_was_anything.wasAI = False
    user_was_anything.wasHitler = False
    user_was_anything.wasNecoarc = False
    user_was_anything.wasMagnumJopus = False
    user_was_anything.wasFiftyTwo = False
    user_was_anything.wasSixtyNine = False
    user_was_anything.wasDrugs = False
    user_achievements.old_school = False
    user_achievements.sapper = False
    user_achievements.casino = False
    user_achievements.casino_count = 0
    async with md.async_session() as session:
        #Записываем изменения
        await session.merge(user_achievements)
        await session.merge(user_was_anything)
        await session.merge(user)
        await session.commit() #Сохраняем изменения
    await message.reply("Поздравляю, ты обнулился! Без отцов, без клоунизма, а думать надо было раньше🤡") #Вывод сообщения


@commands_r.message(Command(commands=['idea']))
async def idea(message: Message) -> Any:
    await rq.set_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name) #Записываем пользователя в БД
    load_dotenv()
    await message.forward(chat_id=os.getenv('ADMIN')) #Пересылаем сообщение в отдельный чат по айди
    await message.answer("Не мог получше что-то придумать, лол?🤡 Ладно, ща с максом поржём над этим (и над тобой)") #Отправляем сообщение
