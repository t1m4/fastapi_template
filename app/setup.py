import logging

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from app import reporting
from app.api.api import router
from app.config import settings
from app.exceptions.errors import BaseError


def setup_logging() -> None:
    logging.basicConfig(level=settings.LOG_LEVEL)

    modules = [{'name': 'uvicorn', 'level': settings.LOG_LEVEL}, {'name': 'tests', 'level': logging.INFO}]
    for module in modules:
        logger = logging.getLogger(module['name'])
        logger.setLevel(module['level'])
        log_formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] ' + ' %(module)s - %(name)s: %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)


def setup_error_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseError)
    async def exception_handler(_: Request, exc: BaseError) -> Response:
        return JSONResponse(
            status_code=exc.http_status,
            content={'message': exc.message},
        )


def setup_routes(app: FastAPI) -> None:
    app.include_router(router)


def setup_error_reporting() -> None:
    reporting.init(dsn=settings.SENTRY_DSN, environment=settings.ENVIRONMENT)
