from app.commands.user_command import UserCreateCommand
from app.schemas.db.user import UserDB
from app.schemas.request.user import CreateUserInRequest
from app.selectors.user_selectors import UserSelector


class CreateUserService:
    def __init__(
        self,
        *,
        user_selector: UserSelector,
        create_user_command: UserCreateCommand,
    ) -> None:
        self._user_selector = user_selector
        self._user_command = create_user_command

    async def __call__(self, create_user: CreateUserInRequest) -> UserDB:
        user_id = await self._user_command.create(
            email=create_user.email,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
        )
        """
        ...
        send main and other stuff
        ...
        """
        return await self._user_selector.get(user_id=user_id)
