"""
    This file defines the models used by the user service.
"""

# local imports
from .. import Model
from ..fields import CharField

class User(Model):
    """ The user model used by Synca. """
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    email = CharField(null=False)
