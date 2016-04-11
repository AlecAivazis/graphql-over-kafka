"""
    This service maintains the list of recipes in our cloud.
"""

# third party imports
from nautilus import ModelService
# third party imports
from nautilus.models import BaseModel, CRUDNotificationCreator, fields

class Recipe(BaseModel, CRUDNotificationCreator):
    name = fields.CharField()

class ServiceConfig:
    database_url = 'sqlite:///recipes.db'

class RecipeService(ModelService):
    model = Recipe
    config = ServiceConfig
