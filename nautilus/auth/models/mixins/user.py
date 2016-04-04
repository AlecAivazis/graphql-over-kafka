"""
    This file defines the models used by the user service.
"""

# local imports
from nautilus.models import BaseModel
from nautilus.models.fields import CharField

class User(BaseModel):
    """ The user model used by """
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    email = CharField(null=False)
