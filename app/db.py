from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator

from sqlalchemy import create_engine, orm
from sqlalchemy.engine import Connection, Row

from app.config import config
from app.utils import set_context_var, to_json


class NoDBConnection(Exception):
    ...


_connection_ctx: ContextVar[Connection] = ContextVar("_connection_ctx")


engine = create_engine(
    url=config.DATABASE_URL,
    json_serializer=to_json,
    future=True,
)

Base = orm.declarative_base()


@contextmanager
def connect() -> Iterator[Connection]:
    """
    Open connection to database and store connection into context variable.
    To access context variable use function `db.get_connection()`
    Don't use it for insert/update/delete
    """
    with engine.connect() as connection:
        with set_context_var(var=_connection_ctx, value=connection):
            yield connection


@contextmanager
def begin() -> Iterator[Connection]:
    """Begin transaction"""
    with connect() as connection:
        with connection.begin():
            yield connection


def get_connection() -> Connection:
    try:
        return _connection_ctx.get()
    except LookupError:
        raise NoDBConnection("Database connection not started. " "Use context manager `db.connect()` or `db.begin()`")


def select_all(query: Any) -> list[Row]:
    connection = get_connection()
    result = connection.execute(query)
    return result.all()


def select_one(query: Any) -> Row | None:
    connection = get_connection()
    result = connection.execute(query)
    return result.first()


def select_scalar(query: Any) -> Any:
    connection = get_connection()
    result = connection.execute(query)
    return result.scalar_one()


def execute(query: Any) -> None:
    connection = get_connection()
    connection.execute(query)
