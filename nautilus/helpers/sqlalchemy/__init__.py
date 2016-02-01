# third party imports
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.jsontools import JsonSerializableBase
from sqlalchemy.ext.declarative import declarative_base

# local imports
from .typeDecorators import Password
from .mixins import *
from ...ext import db

JsonBase = declarative_base(cls=(JsonSerializableBase,))


class BaseModel(db.Model, JsonBase):

    def __init__(self, **kwargs):
        """ treat kwargs as attribute assignment """
        # loop over the given kwargs
        for key, value in kwargs.items():
            # treat them like attribute assignments
            setattr(self, key, value)

    def save(self):
        # add the entry to the db session
        db.session.add(self)
        # commit the entry
        db.session.commit()


    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8')
