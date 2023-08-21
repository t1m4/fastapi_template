from collections.abc import Generator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from app.db.tables.user import User
from app.exceptions.errors import DoesNotExistsError
from app.schemas.db.user import UserDB


class UserSelector:
    _model = User

    def __init__(self, session_factory: async_scoped_session) -> None:
        self.session_factory = session_factory

    async def list(self) -> Generator[UserDB]:
        async with self.session_factory() as session:
            stream = await session.stream_scalars(select(self._model).order_by(self._model.id))
            async for row in stream:
                yield UserDB.from_orm(row)

    async def get(self, user_id: int) -> UserDB:
        async with self.session_factory() as session:
            user_data = await session.scalar(
                select(self._model).where(self._model.id == user_id).order_by(self._model.id)
            )
        if not user_data:
            raise DoesNotExistsError
        return UserDB.from_orm(user_data)
