from celery import Celery, signals

from app.config import config


@signals.worker_process_init.connect()
def start_worker_process(*args: tuple, **kwargs: dict) -> None:
    """Some job on worker start"""


@signals.worker_process_shutdown.connect()
def stop_worker_process(*args: tuple, **kwargs: dict) -> None:
    """Some job on worker stop"""


celery_app = Celery(main='fastapi_template', broker=config.REDIS_URL)
celery_app.autodiscover_tasks()
