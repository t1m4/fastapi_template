import logging

from app.worker.worker import celery_app as app

logger = logging.getLogger(__name__)


@app.task
def test_task(name: str = "World") -> None:
    logger.info(f"Hello, {name}")
