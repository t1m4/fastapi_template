import asyncio
import logging

import sqlalchemy
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.containers import Container
from app.db.database import Database
from app.types import StrDict
from app.worker.tasks import test_task

router = APIRouter()

logger = logging.getLogger(__name__)


async def test_create_new_session_factory(session_factory):
    print('\nTest create new session in another task')
    print('Current task', id(asyncio.current_task()))
    await asyncio.sleep(0)
    print(len(session_factory.__dict__['registry'].registry), 'Will be: 1')
    async with session_factory() as session:
        async with session.begin():
            await session.execute(sqlalchemy.text('SELECT 1 = 1;'))
    print(len(session_factory.__dict__['registry'].registry), "Will be: 2")

async def test_use_same_session(session_factory, session):
    print('\nTest use same session')
    print(len(session_factory.__dict__['registry'].registry), 'Will be: 1')
    async with session.begin():
        await session.execute(sqlalchemy.text('SELECT 1 = 1;'))
    print(len(session_factory.__dict__['registry'].registry), "Will be: 1")

@router.get(path='/test_async_scoped')
@inject
async def health(db: Database = Depends(Provide[Container.db])) -> StrDict:
    print('view task', id(asyncio.current_task()))
    async with db.async_engine.connect() as conn:
        await conn.execute(sqlalchemy.text('SELECT 1 = 1;'))
        await conn.execute(sqlalchemy.text('select pg_sleep(1);'))

    print(len(db.session_factory.__dict__['registry'].registry), 'Will be 0.', db.session_factory.__dict__['registry'].registry)
    print('Create new session', db.session_factory.__dict__['registry']())
    print(len(db.session_factory.__dict__['registry'].registry), 'Will be: 1', db.session_factory.__dict__['registry'].registry)
    async with db.session_factory() as session:
        async with session.begin():
            await session.execute(sqlalchemy.text('SELECT 1 = 1;'))
        async with session.begin():
            await session.execute(sqlalchemy.text('SELECT 1 = 1;'))
        
        await asyncio.gather(*[test_use_same_session(db.session_factory, session)])

    print(len(db.session_factory.__dict__['registry'].registry), 'Will be: 1. Use the same one for current task')
    tasks = [asyncio.create_task(test_create_new_session_factory(db.session_factory))]
    print('before sleep')
    await asyncio.sleep(5)
    print('after sleep')
    await asyncio.gather(*tasks)
        
    # await test_create_new_session_factory(db.session_factory)

    return {'status': 'alive'}

@router.get(path='/health')
@inject
async def health(db: Database = Depends(Provide[Container.db])) -> StrDict:
    async with db.async_engine.connect() as conn:
        await conn.execute(sqlalchemy.text('SELECT 1 = 1;'))
    async with db.session() as session:
        await session.execute(sqlalchemy.text('SELECT 1 = 1;'))
    return {'status': 'alive'}


@router.get('/')
async def root() -> StrDict:
    logger.debug('DEBUG MESSAGE')
    logger.info('INFO MESSAGE')
    logger.warning('WARNING MESSAGE')
    logger.error('ERROR MESSAGE')
    test_task.delay()
    return {'message': 'Hello World!'}


@router.get('/hello/{name}')
async def say_hello(name: str) -> StrDict:
    return {'message': f'Hello {name}'}
