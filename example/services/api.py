from nautilus import APIGateway
from graphene import Schema, ObjectType, String
from nautilus.api import ServiceObjectType
from nautilus.api.fields import Connection


# create the schema based on the query object
schema = Schema(name='Product Schema')

## define the schema that encapsulates the cloud

class Recipe(ServiceObjectType):

    class Meta:
        service = 'recipe'

    name = String(description = 'The name of the recipe')
    ingredients = Connection('Ingredient', description = 'The ingredients in this recipe.')



class Ingredient(ServiceObjectType):

    class Meta:
        service = 'ingredient'

    name = String(description = 'The name of the ingredient')
    recipes = Connection(Recipe, description = 'The recipes with this ingredient')


# add the query to the schema
schema.query = Query

# create a nautilus service with just the schema
service = APIGateway(schema=schema)
