import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from starlette.testclient import TestClient

from app import db
from app.main import create_app


@pytest.fixture(scope="session", autouse=True)
def app():
    yield create_app()


@pytest.fixture(scope="session")
def client(app: FastAPI):
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def db_cleanup():
    """Automatically cleanup database after every tests"""
    try:
        yield
    finally:
        with db.begin() as connection:
            tables = ", ".join(db.Base.metadata.tables)
            connection.execute(sa.text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE;"))
