# external imports
from playhouse.signals import Model
import peewee
# local imports
from ..db import db

class _Meta(type):
    """
        The base metaclass for the nautilus models.
    """

    def __init__(self, name, bases, attributes):
        # create the super class
        super().__init__(name, bases, attributes)

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
        self.model_name = name


class _MixedMeta(_Meta, peewee.BaseModel):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """

class BaseModel(Model, metaclass=_MixedMeta):

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
