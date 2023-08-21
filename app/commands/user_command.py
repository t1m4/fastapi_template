from sqlalchemy.ext.asyncio import async_scoped_session

from app.db.tables.user import User


class UserCreateCommand:
    _model = User

    def __init__(self, session_factory: async_scoped_session) -> None:
        self.session_factory = session_factory

    async def create(
        self,
        email: str,
        first_name: str,
        last_name: str,
    ) -> int | None:
        user = self._model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        async with self.session_factory() as session, session.begin():
            session.add(user)
            await session.flush()
        return user.id
