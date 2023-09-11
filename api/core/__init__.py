from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core import utils

db_login = utils.get_db_login()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
    db_login[0], db_login[1], db_login[2], db_login[3], db_login[4]) 
    #"postgres", "sat123", "localhost", "5432", "postgres")
db = SQLAlchemy(app)

from core import routes
