# third party imports
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.jsontools import JsonSerializableBase
from sqlalchemy.ext.declarative import declarative_base

# local imports
from .typeDecorators import Password
from .mixins import *
from ...ext import db, admin

JsonBase = declarative_base(cls=(JsonSerializableBase,))

class Meta(type):
    """
        The base metaclass for the nautilus models. Currently, it's primary use is to
        automatically register a model class with the admin after it is created.
    """

    def __new__(cls, name, bases, attributes, **kwds):
        """ Called after the class record is created. """

        # if the cls doesn't have the attribute yet, then it must be the first
        if not hasattr(cls, 'is_base'):
            # mark the initial class
            cls.is_base = True
            attributes['is_base'] = True
        # otherwise we are a sub class
        else:
            attributes['is_base'] = False

        # create the next class record
        return super().__new__(cls, name, bases, attributes, **kwds)


class MixedMeta(Meta, type(db.Model)):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """
    def __init__(self, name, bases, attributes, **kwds):
        super().__init__(name, bases, attributes, **kwds)
        # if we are the sub class of a derived one
        if not attributes['is_base']:
            # let the user handle
            # admin.add_model(self)
            self.onCreation()


class BaseModel(db.Model, JsonBase, metaclass=MixedMeta):

    def __init__(self, **kwargs):
        """ treat kwargs as attribute assignment """
        # loop over the given kwargs
        for key, value in kwargs.items():
            # treat them like attribute assignments
            setattr(self, key, value)

    @classmethod
    def onCreation(cls):
        # register the class with the admin interface
        admin.add_model(cls)


    def save(self):
        # add the entry to the db session
        db.session.add(self)
        # commit the entry
        db.session.commit()


    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8')
