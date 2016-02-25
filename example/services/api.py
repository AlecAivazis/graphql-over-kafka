# external imports
from nautilus import APIGateway
from graphene import Schema, ObjectType, String, Mutation, Boolean
from nautilus.api import ServiceObjectType
from nautilus.api.fields import Connection
from nautilus.network import dispatchAction
from nautilus.conventions import getCRUDAction
# local imports
from .recipes import service as RecipeService
from .ingredients import service as IngredientService


# create the schema based on the query object
schema = Schema(name='Product Schema')


## define the schema that encapsulates the cloud

class Recipe(ServiceObjectType):

    class Meta:
        service = RecipeService
    
    # connections are resolved/joined using the appropriate connection service
    # you can avoid circular/undefined references using strings - nautilus will look 
    # for the corresponding ServiceObjectType
    ingredients = Connection('Ingredient', description = 'The ingredients in this recipe.')



class Ingredient(ServiceObjectType):

    class Meta:
        service = IngredientService
    
    recipes = Connection(Recipe, description = 'The recipes with this ingredient')


# add the query to the schema
schema.query = Query


# third party imports

class AddRecipeMutation(Mutation):

    class Input:
        name = String()

    success = Boolean(description="Wether or not the dispatch was successful")

    @classmethod
    def mutate(cls, instance, args, info):
        """ perform the mutation """
        # send the new production action into the queue
        dispatchAction({
            'type': getCRUDAction('create', 'product'),
            'payload': args
        })


class Mutation(ObjectType):
    """ the list of mutations that the api supports """
    addRecipe = Field(AddRecipeMutation)


sceham.mutation = Mutation

# create a nautilus service with just the schema
service = APIGateway(schema=schema)
