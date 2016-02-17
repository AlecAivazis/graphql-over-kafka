Connecting Services Together
=============================

Given their highly specialized nature, a service is not very useful on its
own. So, let's add another to our example cloud. This is a good opportunity
to use some of the services that nautilus provides which are great starting
points when adding new functionalities to your cloud.


Using Pre-defined Services
---------------------------
One of the most commonly used services is the ModelService which maintains
records of a particular database. If this sounds really familiar, it should
- you implemented 80% of the service in Part 1, it just handles the other
CRUD actions for you.

Before we add another model service, let's rename the ``server.py`` file
from part 1 to ``recipes.py`` and create a new file called ``ingredients.py``
in our directory. Inside of this file, paste the following code:

.. code-block:: python

    # third party imports
    from nautilus import ModelService, ServiceManager
    # third party imports
    from sqlalchemy import Column, Text
    from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

    # the notification mixin adds the sqlalchemy event handlers from part 1
    class Ingredient(CRUDNotificationCreator, HasID, BaseModel):
        name = Column(Text)


    class ServiceConfig:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredients.db'


    service = ModelService(
        model = Ingredient,
        configObject = ServiceConfig,
    )

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()


You can see that we were able to get the same/more functionality as before with
significantly fewer lines of code. If you want, you can run the server
and go to the admin panel / graphql endpoints to verify things are
working as you expect.

Sorry if feel that you went through all that trouble in part 1 for nothing.
At least now you know what's going on underneath and hopefully you never have
to write that much boilerplate again. If you do need to implement a
completely custom service, send me a message and let's work together to figure
out if nautilus can better serve your needs at a framework level.


Connection Models
-------------------

Another very common service in nautilus clouds is the ConnectionService which
is a specialized ModelService whose internal data represents the relationship
between two other services. If you are familiar with databases, connection
services play the exact same role as join tables.

If that made sense to you, feel free to skip this paragraph. To illustrate
the role of connection services, say there is an entry in the recipe table
with and id of 1 and a entry in the ingredient table which also has an id
of 1. To express that the recipe contains a particular ingredient, we would
add an entry in the connection service which has a value of 1 in the recipe
column and a value of 1 in the ingredient column. Keep in mind that these
columns do not necessarily have to be unique. If there was a second ingredient
with id 2 that is also a part of the recipe, there would be a second entry in
the connection service that has a 1 in the recipe column but this time there
would be a 2 in the ingredient column. This relationship is called
"many-to-many" because a recipe can have many ingredients and an ingredient can be a member of many recipes (neither column is unique). Relationships can also be
classified as "one-to-one" and "one-to-many".

Make a new file called ``recipeIngredients.py`` next to the previously created
files. Now, create a ConnectionService to manage the relationship between
recipes and ingredients:

.. code-block:: python

    # external imports
    from nautilus import ConnectionService
    # local imports
    from recipes import service as recipeService
    from ingredients import service ingredientService

    class ServiceConfig:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredients.db'

    service = ConnectionService(
        services = [recipeService, ingredientService],
        configObject = ServiceConfig
    )


Again, you can run the service and check out the various endpoints.

