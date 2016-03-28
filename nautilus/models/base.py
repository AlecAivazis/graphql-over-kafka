# external imports
from playhouse.signals import Model, post_save
# local imports
from nautilus import admin
from ..db import db

class _Meta(type):
    """
        The base metaclass for the nautilus models. Currently, it's primary use is to
        automatically register a model class with the admin after it is created.
    """

    def __init__(self, name, bases, attributes, **kwds):
        # create the super class
        super().__init__(name, bases, attributes, **kwds)

        # for each base we inherit from
        for base in bases:
            # if the base defines some mixin behavior
            if hasattr(base, '__mixin__'):
                # treat the base like a mixin
                base.__mixin__()

        # if this class defines mixin behavior
        if hasattr(self, '__mixin__'):
            # call the callback
            self.__mixin__()
            
        # save the name in the class
        self.name = name


class _MixedMeta(_Meta, type(Model)):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """


class BaseModel(Model, metaclass=_MixedMeta):

    nautilus_base = True # necessary to prevent meta class behavior on this model

    class Meta:
        database = db


    def _json(self):
        # build a dictionary out of just the columns in the table
        return {
            field.name: getattr(self, field.name) \
                for field in type(self).fields()
        }


    @classmethod
    def __mixin__(cls):
        """
            This callback allows for customization of the class record defined
            by various subclass of the base model.
        """


    @classmethod
    def primary_key(cls):
        """
            Retrieve the primary key of the database table.
        """
        return cls._meta.primary_key


    @classmethod
    def required_fields(cls):
        """
            Retrieve the required fields for this model.
        """
        return [field for field in cls.fields() if not field.null]


    @classmethod
    def fields(cls):
        """
            Returns the fields of the table.
        """
        return cls._meta.fields.values()


    __abstract__ = True
