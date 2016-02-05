# external imports
from flask import current_app as currentApp
# local imports
from .services import *

# external imports
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
