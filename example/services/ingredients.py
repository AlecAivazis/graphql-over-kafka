"""
    This service maintains the list of ingredients in our cloud.
"""

# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class Ingredient(CRUDNotificationCreator, HasID, BaseModel):
    name = Column(Text)

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredients.db'

service = ModelService(
    model = Ingredient,
    configObject = ServiceConfig,
)
