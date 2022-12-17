import logging

from fastapi import APIRouter, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from app import reporting
from app.config import config
from app.errors import BaseError
from app.health import handlers as health
from app.users import handlers as users


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)


def setup_error_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseError)
    async def exception_handler(_: Request, exc: BaseError) -> Response:
        return JSONResponse(
            status_code=exc.http_status,
            content={"message": exc.message},
        )


def setup_routes(app: FastAPI) -> None:
    api = APIRouter(prefix=config.BASE_API_PATH)
    api.include_router(health.router)
    api.include_router(users.router)
    app.include_router(api)


def setup_error_reporting() -> None:
    reporting.init(dsn=config.SENTRY_DSN, environment=config.ENVIRONMENT)
