import logging

from celery import Celery
from celery.signals import (
    after_setup_logger,
    after_setup_task_logger,
    worker_process_init,
)

from api.utils.log_formatter import JSONFormatter
from api.utils.redis_config import get_redis_url

logger = logging.getLogger(__name__)


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


@worker_process_init.connect
def _dispose_db_engine_on_fork(**kwargs):
    """Give each prefork worker child its own database connections.

    The engine opens connections in the parent process (scheduler/cache warmup
    at startup); the prefork pool then forks children that inherit those same
    libpq sockets. Disposing the pool in each child forces fresh, per-process
    connections.
    """
    try:
        from api import app
        from api.entrypoints.extensions import db

        with app.app_context():
            # close=False: reset the pool in this child without closing the
            # sockets the parent process still holds
            db.engine.dispose(close=False)
    except Exception as e:  # pragma: no cover - defensive, logged not raised
        logger.error(f"Failed to dispose DB engine on worker init: {e}")


celery = make_celery()
