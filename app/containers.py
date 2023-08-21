from dependency_injector import containers, providers

from app.commands.address_command import (
    BatchCreateAddressCommand,
    BatchUpdateAddressCommand,
)
from app.commands.user_command import UserCreateCommand
from app.config import settings
from app.db.database import Database
from app.selectors.user_selectors import UserSelector
from app.services.address_service import (
    BatchCreateAddressService,
    BatchUpdateAddressService,
)
from app.services.user_service import CreateUserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.DATABASE_URL)

    user_selector = providers.Factory(UserSelector, session_factory=db.provided.session)
    create_user_command = providers.Factory(UserCreateCommand, session_factory=db.provided.session)
    create_user_service = providers.Factory(
        CreateUserService,
        user_selector=user_selector,
        create_user_command=create_user_command,
    )
    batch_create_address_command = providers.Factory(
        BatchCreateAddressCommand, async_engine=db.provided.async_engine, session_factory=db.provided.session
    )
    batch_create_address_service = providers.Factory(
        BatchCreateAddressService,
        batch_create_address_command=batch_create_address_command,
    )

    batch_update_address_command = providers.Factory(
        BatchUpdateAddressCommand, async_engine=db.provided.async_engine, session_factory=db.provided.session
    )
    batch_update_address_service = providers.Factory(
        BatchUpdateAddressService,
        batch_update_address_command=batch_update_address_command,
    )


container = Container()
container.config.from_pydantic(settings)
