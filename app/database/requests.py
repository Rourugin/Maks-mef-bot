from typing import Any
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from app.database.models import User
from app.database.models import async_session


async def set_user(user_id: int, user_name: str, first_name: str, last_name: str) -> Any:
    query = select(User).where(User.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        user = result.scalar()
        if user is not None:
            return None
        obj_user = User(
            user_id=user_id,
            user_name=user_name,
            user_first_name=first_name,
            user_last_name=last_name,
            clownizm=0,
            wasJewish=False,
            wasFDC=False,
            wasNu=False,
            wasGandalf=False,
            wasAI=False,
            wasHitler=False,
            wasNecoarc=False,
            wasMagnumJopus=False,
            wasFiftyTwo=False,
            wasSixtyNine=False
        )
        session.add(obj_user)
        await session.commit()


async def get_user(user_id: int) -> User | None:
    query = select(User).where(User.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        try:
            return result.scalar()
        except NoResultFound:
            return None


async def get_all_users() -> list[dict]:
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        users_dict = [user.to_dict() for user in users]
        sorted_users = sorted(users_dict, key=lambda x: x['clownizm'], reverse=True)
        return sorted_users


async def count_users() -> int:
    async with async_session() as session:
        users = await session.execute(select(func.count()).select_from(User))
        return users.scalar()