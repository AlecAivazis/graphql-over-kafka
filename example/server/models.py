"""
    This file defines the models used by the recipe service.
"""

# third party imports
from sqlalchemy import Column, Text
from nautilus.helpers.sqlalchemy import BaseModel, HasID, CRUDNotificationCreator

# CRUDNotificationCreator - automatically dispatches appropriate actions when records are C*UDed
# HasID - adds an auto-incrementing, primary_key field called `id` to the model
# BaseModel - provides basic functionalities like auto-admin registration and kwarg constructors
class Recipe(CRUDNotificationCreator, HasID, BaseModel):
    name = Column(Text)
    description = Column(Text)
