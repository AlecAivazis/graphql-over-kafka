# third party imports
import nautilus
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.jsontools import JsonSerializableBase
from sqlalchemy.ext.declarative import declarative_base
from nautilus.ext import db

# local imports
from .typeDecorators import Password
from .mixins import *

JsonBase = declarative_base(cls=(JsonSerializableBase,))


class BaseModel(JsonBase, nautilus.ext.db.Model):
    """Convenience base DB model class. Makes sure tables in MySQL are created as InnoDB.
    This is to enforce foreign key constraints (MyISAM doesn't support constraints) outside of production. Tables are
    also named to avoid collisions.
    """

    def save(self):
        # add the entry to the db session
        db.session.add(self)
        # commit the entry
        db.session.commit()

    @declared_attr
    def __tablename__(self):
        return '{}_{}'.format(self.__module__.split('.')[-1], self.__name__.lower())

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8')
