from app.schemas.db.address_db import AddressDB
from app.schemas.request.address_request import AddressCreateRequest
from polyfactory.factories.pydantic_factory import ModelFactory
from app.containers import container
import sqlalchemy as sa
from app.db.tables.address import Address as AddressTable
from polyfactory import AsyncPersistenceProtocol


class AddressCreateRequestFactory(ModelFactory[AddressCreateRequest]):
    __model__ = AddressCreateRequest


class AsyncPersistenceHandler(AsyncPersistenceProtocol[AddressDB]):
    async def save(self, data: AddressDB) -> AddressDB:
        async_engine = container.db.provided.async_engine()
        async with async_engine.begin() as connection:
            user_cursor = await connection.execute(sa.insert(AddressTable).values(data.dict()).returning(AddressTable))
            user_row = user_cursor.first()
            return AddressDB.from_orm(user_row)

    async def save_many(self, data: list[AddressDB]) -> list[AddressDB]:
        users = [user.dict() for user in data]
        async_engine = container.db.provided.async_engine()
        async with async_engine.begin() as connection:
            users_rows = (await connection.execute(sa.insert(AddressTable).returning(AddressTable), users)).all()
            users = [AddressDB.from_orm(user_row) for user_row in users_rows]
        return users


class AddressFactory(ModelFactory[AddressDB]):
    __model__ = AddressDB
    __async_persistence__ = AsyncPersistenceHandler

    @classmethod
    async def get(cls, address_id: int) -> AddressDB | None:
        async_engine = container.db.provided.async_engine()
        async with async_engine.connect() as connection:
            address_row = (await connection.execute(sa.select(AddressTable).where(AddressTable.id == address_id))).first()
        return AddressDB.from_orm(address_row) if address_row else None

    @classmethod
    async def all(cls) -> list[AddressDB]:
        async_engine = container.db.provided.async_engine()
        addresses = []
        async with async_engine.connect() as connection:
            addresses_rows = (await connection.execute(sa.select(AddressTable))).all()
        for address_row in addresses_rows:
            addresses.append(AddressDB.from_orm(address_row))
        return addresses
