from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger

from api.utils.log_formatter import JSONFormatter
from api.utils.redis_config import get_redis_url


def make_celery(app_name=__name__) -> Celery:
    redis_url = get_redis_url()
    celery_app = Celery(app_name, broker=redis_url, backend=redis_url)
    celery_app.set_default()
    return celery_app


def _apply_json_formatter(logger, **kwargs):
    formatter = JSONFormatter()
    for handler in logger.handlers:
        handler.setFormatter(formatter)


after_setup_logger.connect(_apply_json_formatter)
after_setup_task_logger.connect(_apply_json_formatter)

celery = make_celery()
