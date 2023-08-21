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
