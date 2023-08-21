import logging

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, async_scoped_session

from app.db.tables.address import Address
from app.db.tables.user import User
from app.exceptions.errors import DoesNotExistsError
from app.schemas.db.address_db import AddressDB
from app.schemas.request.address_request import (
    AddressCreateRequest,
    AddressUpdateRequest,
)

logger = logging.getLogger(__name__)


class BatchCreateAddressCommand:
    def __init__(self, async_engine: AsyncEngine, session_factory: async_scoped_session) -> None:
        self.async_engine = async_engine
        self.session_factory = session_factory

    async def batch_create(self, user_id: int, addresses: list[AddressCreateRequest]) -> list[AddressDB]:
        logger.debug('Create %s addresses for user %s', len(addresses), user_id)
        async with self.session_factory() as session, session.begin():
            get_user_query = sa.select(User.id).where(User.id == user_id).with_for_update()
            user = await session.scalar(get_user_query)
            if not user:
                raise DoesNotExistsError
            db_addresses = []
            for address in addresses:
                db_address = Address(user_id=user_id, email_address=address.email_address)
                session.add(db_address)
                db_addresses.append(db_address)
            await session.flush()

            result = []
            for row in db_addresses:
                result.append(AddressDB.from_orm(row))
        return result

    async def batch_create_using_core(self, user_id: int, addresses: list[AddressCreateRequest]) -> list[AddressDB]:
        async with self.async_engine.begin() as connection:
            get_user_query = sa.select(User.id).where(User.id == user_id).with_for_update()
            user = await connection.scalar(get_user_query)
            if not user:
                raise DoesNotExistsError

            db_addresses = []
            for address in addresses:
                db_address = {'user_id': user_id, 'email_address': address.email_address}
                db_addresses.append(db_address)
            stream = await connection.execute(sa.insert(Address).values(db_addresses).returning(Address))
            result = []
            for row in stream:
                result.append(AddressDB.from_orm(row))
        return result


class BatchUpdateAddressCommand:
    def __init__(self, async_engine: AsyncEngine, session_factory: async_scoped_session) -> None:
        self.async_engine = async_engine
        self.session_factory = session_factory

    async def batch_update(self, user_id: int, addresses: list[AddressUpdateRequest]) -> list[int]:
        addresses_ids = []
        db_addresses = []
        for address in addresses:
            addresses_ids.append(address.id)
            db_address = {'id': address.id, 'email_address': address.email_address}
            db_addresses.append(db_address)
        async with self.session_factory() as session, session.begin():
            get_user_query = sa.select(User.id).where(User.id == user_id).with_for_update()
            user = await session.scalar(get_user_query)
            if not user:
                raise DoesNotExistsError

            query = sa.select(sa.func.count(Address.id)).where(Address.id.in_(addresses_ids))
            addresses_count = await session.scalar(query)
            if addresses_count != len(addresses_ids):
                raise DoesNotExistsError

            await session.execute(sa.update(Address), db_addresses)
            stream = await session.scalars(sa.select(Address).where(Address.id.in_(addresses_ids)))
            result = []
            for row in stream.all():
                result.append(AddressDB.from_orm(row))
        return result

    async def batch_update_with_core(self, user_id: int, addresses: list[AddressUpdateRequest]) -> list[int]:
        db_addresses = []
        addresses_ids = []
        for address in addresses:
            addresses_ids.append(address.id)
            db_address = {'id': address.id, 'email_address': address.email_address}
            db_addresses.append(db_address)
        async with self.async_engine.begin() as connection:
            get_user_query = sa.select(User.id).where(User.id == user_id).with_for_update()
            user = await connection.scalar(get_user_query)
            if not user:
                raise DoesNotExistsError

            query = sa.select(sa.func.count(Address.id)).where(Address.id.in_(addresses_ids))
            addresses_count = await connection.scalar(query)
            if addresses_count != len(addresses_ids):
                raise DoesNotExistsError

            address_bindparams = {}
            for field_name in AddressUpdateRequest.__fields__:
                address_bindparams[field_name] = sa.bindparam(field_name)
            query = sa.update(Address).where(Address.id == sa.bindparam('id')).values(**address_bindparams)
            await connection.execute(query, db_addresses)
            stream = await connection.execute(sa.select(Address).where(Address.id.in_(addresses_ids)))
            result = []
            for row in stream.all():
                result.append(AddressDB.from_orm(row))
        return result
