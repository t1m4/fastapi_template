from typing import List
from fastapi import FastAPI
import sqlalchemy as sa
from polyfactory.factories.pydantic_factory import ModelFactory

from app.containers import container
from app import db
from app.db.tables.user import User as UserTable
from app.schemas.db.user import UserDB
from app.schemas.request.user import CreateUserInRequest
from sqlalchemy.ext.asyncio import AsyncEngine
from polyfactory import AsyncPersistenceProtocol, SyncPersistenceProtocol


class CreateUserInRequestFactory(ModelFactory[CreateUserInRequest]):
    __model__ = CreateUserInRequest



class AsyncPersistenceHandler(AsyncPersistenceProtocol[UserDB]):
    async def save(self, data: UserDB) -> UserDB:
        async_engine = container.db.provided.async_engine()
        async with async_engine.begin() as connection:
            user_cursor = await connection.execute(sa.insert(UserTable).values(data.dict()).returning(UserTable))
            user_row = user_cursor.first()
            return UserDB.from_orm(user_row)

    async def save_many(self, data: List[UserDB]) -> List[UserDB]:
        users = [user.dict() for user in data]
        async_engine = container.db.provided.async_engine()
        async with async_engine.begin() as connection:
            users_rows = (await connection.execute(sa.insert(UserTable).returning(UserTable), users)).all()
            users = [UserDB.from_orm(user_row) for user_row in users_rows]
        return users


class UserFactory(ModelFactory[UserDB]):
    __model__ = UserDB
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    async def get(cls, user_id: int) -> UserDB | None:
        async_engine = container.db.provided.async_engine()
        async with async_engine.connect() as connection:
            user_row = (await connection.execute(sa.select(UserTable).where(UserTable.id == user_id))).first()
        return UserDB.from_orm(user_row) if user_row else None
