"""
    This file defines the models used by the user service.
"""

# local imports
from ..base import BaseModel
from ..fields import CharField

class User(BaseModel):
    """ The user model used by Synca. """
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    email = CharField(null=False)
