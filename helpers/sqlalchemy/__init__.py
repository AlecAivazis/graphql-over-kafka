# third party imports
import nautilus
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
# local imports
from .typeDecorators import Password
from .mixins import HasPassword

class BaseModel(nautilus.ext.db.Model):
    """Convenience base DB model class. Makes sure tables in MySQL are created as InnoDB.
    This is to enforce foreign key constraints (MyISAM doesn't support constraints) outside of production. Tables are
    also named to avoid collisions.
    """

    @declared_attr
    def __tablename__(self):
        return '{}_{}'.format(self.__module__.split('.')[-1], self.__name__.lower())

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8')
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
