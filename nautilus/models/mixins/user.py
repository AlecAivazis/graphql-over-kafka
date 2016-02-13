"""
    This file defines the models used by the user service.
"""

# external imports
from sqlalchemy import Column, Text
from .hasID import HasID

class User(HasID):
    """ The user model used by Synca. """
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text, nullable = False)
