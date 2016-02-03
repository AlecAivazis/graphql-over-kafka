"""
    This file defines the models used by the sensor service.
"""

# third party imports
from sqlalchemy import Column, Text
from nautilus.helpers.sqlalchemy import BaseModel, HasID, CRUDNotificationCreator

# CRUDNotificationCreator - automatically sends actions over the message queue when records are C*UDed
# HasID - adds an auto-increment id primary_key field to the model
# BaseModel - provides basic functionalities like auto-admin registration and kwarg constructors
class Recipe(CRUDNotificationCreator, HasID, BaseModel):
    """ The Sensor model used by Synca. """
    name = Column(Text)
    description = Column(Text)
