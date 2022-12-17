from fastapi import FastAPI

from app import setup
from app.config import config


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.APP_TITLE,
        docs_url=f"{config.BASE_API_PATH}/docs/ui",
    )

    setup.setup_error_reporting()
    setup.setup_logging()
    setup.setup_error_handler(app)
    setup.setup_routes(app)
    return app
