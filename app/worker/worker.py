from celery import Celery, signals

from app.config import settings


@signals.worker_process_init.connect()
def start_worker_process(*args: tuple, **kwargs: dict) -> None:
    """Some job on worker start"""


@signals.worker_process_shutdown.connect()
def stop_worker_process(*args: tuple, **kwargs: dict) -> None:
    """Some job on worker stop"""


celery_app = Celery(main='fastapi_template', broker=settings.REDIS_URL)
celery_app.conf.update(broker_connection_retry_on_startup=True)
celery_app.autodiscover_tasks()
