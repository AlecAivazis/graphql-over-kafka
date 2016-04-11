# external imports
import peewee
# local imports
from ..database import db

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
                base.__mixin__(self)

        # save the name in the class
        self.model_name = name


class _MixedMeta(_Meta, peewee.BaseModel):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """

class BaseModel(peewee.Model, metaclass=_MixedMeta):

    class Meta:
        database = db


    def _json(self):
        # build a dictionary out of just the columns in the table
        return {
            field.name: getattr(self, field.name) \
                for field in type(self).fields()
        }


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
