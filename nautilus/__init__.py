# external imports
from flask import current_app as currentApp
from sqlalchemy import MetaData
# local imports
from .services import *

# external imports
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
