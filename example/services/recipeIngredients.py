from nautilus import ConnectionService
# import the services to connect
from .ingredients import IngredientService
from .recipes import RecipeService

class ServiceConfig:
    database_url = 'sqlite:///ingredientRecipeConnections.db'

class Ingredients(ConnectionService):
    to_serivce = ('Ingredient',)
    from_service = ('Recipe',)

    config = ServiceConfig
