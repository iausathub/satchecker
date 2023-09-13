from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from core import utils
from core.extensions import db

#db_login = utils.get_db_login()

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per second", "2000 per minute"]
)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
    #db_login[0], db_login[1], db_login[2], db_login[3], db_login[4]) 
    #test
    "postgres", "sat123", "localhost", "5432", "postgres") 
db.init_app(app)

from core import routes
