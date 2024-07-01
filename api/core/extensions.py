from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

limiter = Limiter(
    key_func=get_remote_address, default_limits=["100 per second", "2000 per minute"]
)
