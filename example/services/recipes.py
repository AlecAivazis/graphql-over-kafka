"""
    This service maintains the list of recipes in our cloud.
"""

# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class Recipe(CRUDNotificationCreator, HasID, BaseModel):
    name = Column(Text)

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/recipes.db'

service = ModelService(
    model = Recipe,
    configObject = ServiceConfig,
)
