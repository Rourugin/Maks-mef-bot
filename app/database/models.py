import os
from sqlalchemy import inspect
from dotenv import load_dotenv
from typing import Annotated, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

#Создание БД по адресу из .env
load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
async_session = async_sessionmaker(engine)
#Создание своего типа данных (primary_key=True, делает так, чтобы номер строки никогда не повторялся в таблице)
intpk = Annotated[int, mapped_column(primary_key=True)]

#Базовый класс, от которого будут образованы другие (имеет общие параметры всех классов)
class Base(AsyncAttrs, DeclarativeBase):
    pass

#Класс с основной информацией об игроке
class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    user_id: Mapped[int]
    user_first_name: Mapped[Optional[str]]
    user_last_name: Mapped[Optional[str]]
    clownizm: Mapped[int]
    stepfathers: Mapped[int]
    lear: Mapped[int]
    pet: Mapped[int]
    sapper_words: Mapped[int]
    #Функция возвращает АБСОЛЮТНО ВСЕ строки и ячейки БД с классом User
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

#Класс для внезапных событий (регулирует может ли появится событие или оно уже произошло)
class WasAnything(Base):
    __tablename__ = 'wasAnything'

    id: Mapped[intpk]
    user_id: Mapped[int]
    user_first_name: Mapped[Optional[str]]
    user_last_name: Mapped[Optional[str]]
    wasSucked: Mapped[bool]


#Таблица с ачивками (принцип, как WasAnything)
class Achievements(Base):
    __tablename__ = 'achiements'

    id: Mapped[intpk]
    user_id: Mapped[int]
    old_school: Mapped[bool]
    sapper: Mapped[bool]
    casino: Mapped[bool]
    casino_count: Mapped[int]

#Создаёт БД со всеми классами, которые мы объявили в этом файле
async def async_main() -> None:
    async with engine.begin() as conn:
	    await conn.run_sync(Base.metadata.create_all)
