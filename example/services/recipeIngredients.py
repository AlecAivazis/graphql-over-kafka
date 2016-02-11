from nautilus import ConnectionService

# import the services to connect
from .ingredients import service as IngredientService
from .recipes import service as RecipeService

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredientRecipeConnections.db'

service = ConnectionService(
    services = [IngredientService, RecipeService],
    configObject = ServiceConfig
)
