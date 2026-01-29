from celery import Celery

from api.utils.redis_config import get_redis_url


def make_celery(app_name=__name__) -> Celery:
    redis_url = get_redis_url()
    celery_app = Celery(app_name, broker=redis_url, backend=redis_url)
    celery_app.set_default()
    return celery_app


celery = make_celery()
