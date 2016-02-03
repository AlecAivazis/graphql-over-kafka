"""
    The action handler for the Recipe service
"""

from .models import Recipe

# this will be replaced with a generic CRUDActionHandler factory

def actionHandler(type, payload):

    # if the payload represents a new Recipe
    if type == 'create_recipe':
        # if a uuid was not supplied for the Recipe
        if not 'name' in payload:
            # dont do anything
            return

        # create a Recipe instance
        newRecipe = Recipe(**payload)

        # save the new Recipe
        newRecipe.save()
