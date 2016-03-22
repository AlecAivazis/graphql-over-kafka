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
        # if the class is not a nautilus base class
        if 'nautilus_base' not in attributes or not attributes['nautilus_base']:
            # perform the necessary functions
            self.on_creation()

        return

class _MixedMeta(_Meta, type(Model)):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """


class BaseModel(Model, metaclass=_MixedMeta):

    nautilus_base = True # necessary to prevent meta class behavior on this model

    # def __init__(self, **kwargs):
    #     """ treat kwargs as attribute assignment """
    #     # loop over the given kwargs
    #     for key, value in kwargs.items():
    #         # treat them like attribute assignments
    #         setattr(self, key, value)

    class Meta:
        database = db


    def _json(self):
        # build a dictionary out of just the columns in the table
        return {
            field.name: getattr(self, field.name) \
                for field in type(self).fields()
        }


    @classmethod
    def on_creation(cls):
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

