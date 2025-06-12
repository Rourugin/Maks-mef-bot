from typing import Any
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from app.database.models import Base, User, WasAnything, Achievements
from app.database.models import async_session

#Создаём пользователя в БД
async def set_user(user_id: int, first_name: str, last_name: str) -> Any:
    #Пытаемся достать строку из БД по айди (у каждого пользователя оно своё)
    user_query = select(User).where(User.user_id == user_id)
    wasAnything_query = select(WasAnything).where(WasAnything.user_id == user_id)
    achievements_query = select(Achievements).where(Achievements.user_id == user_id)
    async with async_session() as session:
        user_result = await session.execute(user_query)
        wasAnything_result = await session.execute(wasAnything_query)
        achievements_result = await session.execute(achievements_query)
        user = user_result.scalar()
        wat = wasAnything_result.scalar()
        achievements = achievements_result.scalar()
        #Если ничего не находит, то создаётся строка в БД, если что-то есть, то пропуск
        if user is not None:
            pass
        elif user is None:
            obj_user = User(
                user_id=user_id,
                user_first_name=first_name,
                user_last_name=last_name,
                clownizm=0,
                stepfathers=0,
                lear=0,
                pet=0,
                sapper_words=0
            )
            session.add(obj_user)
        if wat is not None:
            pass
        elif wat is None:
            obj_wasAnything = WasAnything(
                user_id=user_id,
                user_first_name=first_name,
                user_last_name=last_name,
                wasSucked=False
            )
            session.add(obj_wasAnything)
        if achievements is not None:
            pass
        elif achievements is None:
            obj_achievements = Achievements(
                user_id=user_id, 
                old_school=False,
                sapper=False,
                casino=False,
                casino_count=0
            )
            session.add(obj_achievements)
        await session.commit() #Сохраняем всё в БД


#Достаём объект (любого класса) из БД по айди
async def get_obj(user_id: int, obj_class: type[Base]) -> Base | None:
    query = select(obj_class).where(obj_class.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        try:
            return result.scalar()
        except NoResultFound:
            return None

#Достаём абсолютно все Элементы из БД с классом User
async def get_all_users() -> list[dict]:
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        users_dict = [user.to_dict() for user in users]
        sorted_users = sorted(users_dict, key=lambda x: x['clownizm'], reverse=True)
        return sorted_users

#Возвращает кол-во строк в БД с классом User
async def count_users() -> int:
    async with async_session() as session:
        users = await session.execute(select(func.count()).select_from(User))
        return users.scalar()