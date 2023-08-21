import asyncio
import logging
from pydantic import PostgresDsn
import pytest
import pytest_asyncio
import sqlalchemy as sa
from fastapi import Depends, FastAPI
from starlette.testclient import TestClient
from dependency_injector.wiring import Provide, inject
from dependency_injector import containers, providers

from app.config import settings
from app.containers import Container
from app.db.database import Database
from app.main import create_app
from app.db.tables.base import Base 
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.tables.base import Base 
from sqlalchemy.ext.asyncio import AsyncEngine
from app.containers import container
from dependency_injector.providers import ProvidedInstance
logger = logging.getLogger(__name__)

TABLE_NAMES = ", ".join(Base.metadata.tables)


def pytest_addoption(parser):
    parser.addoption(
        '--reuse-db', action='store_true', default=False, help='Flag for reuse existing database',
    )
    parser.addoption(
        '--without-db', action='store_true', default=False, help='Flag for unit tests without database',
    )

@pytest.fixture(autouse=True, scope="session")
def app():
    yield create_app()


@pytest.fixture(scope="session")
def client(app: FastAPI):
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True, scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()



async def run_migrations(db_url: PostgresDsn):
    async_engine = create_async_engine(db_url, isolation_level='AUTOCOMMIT')
    async with async_engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await async_engine.dispose()

async def create_test_database_dependency(db_url: PostgresDsn) -> Database:
    database = Database(db_url=db_url)
    container.db.override(database)
    return database


@pytest.fixture(autouse=True, scope='session')
async def test_database(worker_id: str, request: pytest.FixtureRequest):
    """
    Create test database. 
    If option --without-db is action then don't create database.
    If option --reuse-db is active then reuse existing database, overwise delete test in the end of each test session
    In parallel tests each db created using worker_id
    In unit tests don't create db
    """
    if request.config.getoption('--without-db'):
        yield
        return
    is_reuse_db = request.config.getoption('--reuse-db')
    db_params = dict(
        scheme='postgresql+psycopg',
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )
    if worker_id == 'master':
        # if running only one process
        test_database_name = f'{settings.POSTGRES_DB}_test'
    else:
        test_database_name = f'{settings.POSTGRES_DB}_{worker_id}'
    base_db_url = PostgresDsn.build(**db_params)
    db_url = PostgresDsn.build(**db_params, path=f'/{test_database_name}')

    # TODO split to functions
    base_engine = create_async_engine(base_db_url, isolation_level='AUTOCOMMIT')
    if is_reuse_db:
        async with base_engine.connect() as connection:
            test_database_exist = await connection.scalar(sa.text(f"SELECT COUNT(*) FROM pg_database WHERE datname = '{test_database_name}'"))
            if test_database_exist:
                logger.info('Use existing test db %s', test_database_name)
            else:
                logger.info('Create new test db %s', test_database_name)
                await connection.execute(sa.text(f"CREATE DATABASE {test_database_name}"))
        
        await run_migrations(db_url)
        database = await create_test_database_dependency(db_url)
        yield
        await database.async_engine.dispose()
    else:
        async with base_engine.connect() as connection:
            test_database_exist = await connection.execute(sa.text(f"DROP DATABASE IF EXISTS {test_database_name}"))
            logger.info('Create new test db %s', test_database_name)
            await connection.execute(sa.text(f"CREATE DATABASE {test_database_name}"))

        await run_migrations(db_url)
        database = await create_test_database_dependency(db_url)
        yield
        await database.async_engine.dispose()
        async with base_engine.connect() as connection:
            logger.info('Drop test db %s', test_database_name)
            test_database_exist = await connection.execute(sa.text(f"DROP DATABASE IF EXISTS {test_database_name}"))
    await base_engine.dispose()



@pytest.fixture(autouse=True,)
async def db_cleanup(request: pytest.FixtureRequest):
    """Automatically cleanup database after every tests using TRUNCATE"""
    if request.config.getoption('--without-db'):
        yield
        return
    try:
        yield
    finally:
        # NOTE: getting dependency attributes from container
        async_engine = container.db.provided.async_engine()
        async with async_engine.begin() as connection:
            await connection.execute(sa.text(f"TRUNCATE {TABLE_NAMES} RESTART IDENTITY CASCADE;"))
