# external imports
import nautilus
from nautilus import APIGateway

# create an api gateway with just the schema
class RecipeBookAPIGateway(nautilus.APIGateway):

    @nautilus.auth_criteria('Ingredient')
    def auth_ingredient(self, model, user):
        # an ingredient can only be viewed by author
        return model.author == user

# create a service manager to run the service
manager = ServiceManager(RecipeBookAPIGateway)

if __name__ == '__main__':
    manager.run()
