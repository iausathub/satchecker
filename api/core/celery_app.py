from celery import Celery


def make_celery(app_name=__name__) -> Celery:
    celery_app = Celery(
        app_name, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
    )
    celery_app.set_default()
    return celery_app


celery = make_celery()
