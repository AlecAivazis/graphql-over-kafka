Your First Service
===================

Services are the fundamental building blocks for cloud applications powered by
nautilus. Let's begin by creating a directory with an empty file somewhere on
your computer for us to use as a playground.

.. code-block:: bash

    $ mkdir nautilus_playground && \
            cd nautilus_playground && \
            touch server.py

Now that we have a file, let's make our first service. Keep in mind, that
this section is meant to illustrate the various parts of a service, as you
will see in the next section, the service we are about to construct can be
much more succintly created using one of nautilus's pre-packaged services.
Open server.py in your favorite text editor and copy and paste the following:

.. code-block:: python

    from nautilus import Service

    class RecipeService(Service): pass

    if __name__ == '__main__':
        # create an instance of the service
        service = RecipeService()
        # run the http server
        service.run()


Test that this works by executing this script in your console:

.. code-block:: bash

    $ python3 ./server.py


If it complains about permissions, try running ``sudo chmod u+x ./server.py``.
Assuming the regsitry is properly setup (ie consul is running), your terminal
should now indicate that the server started.


Right now, our service is nothing more than a flask application with some
default implementations of basic necessities like security. It doesn't react
to the outside world, it doesn't store any data, nor does it provide
anything for another service to use - let's change that.


Defining a Model
------------------

Now that we have the service defined, let's create a database table
that our service will manage. 

Throughout this guide, we're going to be making a recipe list, so open up
server.py from the previous step and add the Recipe model.

.. code-block:: python

    from nautilus import Service, ServiceManager
    from nautilus.models import BaseModel, fields

    # we're using the HasID mixin here to automatically provide a primary key
    # for the table
    class Recipe(BaseModel):
        name = fields.CharField(help_text="The name of the recipe")

    class RecipeService(Service): pass

    # create a manager for the service
    manager = ServiceManager(RecipeService)

    if __name__ == '__main__':
        manager.run()


Notice we also wrapped the service in a manager, which provides a basic
command line interface for our service.

While our service still can't talk to the outside world, at least it can keep
track of our recipes for us.  Before we can look at the records, we have to
create the database that will persist the data. Since our service is now
wrapped in a manager, we can easily do this by executing the ``syncdb``
command:

.. code-block:: bash

    $ python3 ./server.py syncdb



Building a Schema
-------------------

Traditionally, backend data is made availible via some sort of RESTful api. In
nautilus, services use a piece of technology from the facebook engineers called
GraphQL which allows the service to expose the data through a single endpoint.
For more information on GraphQL, visit [this]() page.

.. code-block:: python

    from nautilus import Service, ServiceManager
    from nautilus.models import BaseModel, fields
    from nautilus.api.fields import Connection
    from nautilus.contrib.graphene_peewee import PeeweeObjectType
    from graphene import Schema

    class Recipe(HasId, BaseModel):
        name = fields.CharField()

    schema = Schema()

    @schema.register
    class RecipeObjectType(PeeweeObjectType):
        """ The GraphQL Object type for our recipes. """
        class Meta:
            model = Recipe

    class Query(graphene.ObjectType):
        """ the root level query for our recipe service """
        recipes = Connection(RecipeObjectType)

        def resolve_recipes(self, args, info):
            """ return all recipes in the database """
            return Recipe.query.all()

    # add the root query to the schema
    schema.query = Query

    class RecipeService(Service):
        schema = schema

    manager = ServiceManager(RecipeService)

    if __name__ == '__main__':
        manager.run()


Note: ``Connection`` is a very special type provided by nautilus.
For now, you can think of it as a wrapper around the List type that
we are using to make our code more easily read.

Sometimes, you might have to create the entire schema by hand, in which case
I suggest reading the graphene documentation [here](graphene). However in most
circumstances, Graphene can create the object for us.


Querying the Service's State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that our service has been given a schema, we can query the internal state
of the service from two different endpoints. Nautilus uses GraphQL as the
service query langauge. Take a second to familiarize yourself with GraphQL
by reading [this]() short blog post.

If you navigate to the root url of your service (``http://localhost:8000`` by
default) you will see that the service  is trying to parse an incoming
query and can't find one. You can give the service a query to fulfill by
padding a value to the `query` url parameter by navigating to a url like
``http://localhost:8000/?query={recipes{ name }}``.

While this does work, it's clear this endpoint is not intended for human
consumption. Instead, if you point your browser to ``/graphiql`` you will
get visual environment for forming queries. I suggest opening a second tab
pointed at the admin interface previously discussed and proving to yourself
that the api is working as expected.


Responding to Actions
-----------------------

Now that our service maintains an internal state and can provide a summary of
that state to other services, all that's left is to provide a way for the
service to mutate its state as it recieves actions. To do this, we
just need to define a function known as the "action handler" that
takes two parameters: ``type`` and ``payload``. ``Type`` identifies
the event and  ``Payload`` provides the associated data. For example,
if an action means to indicate that a new recipe needs to be created,
the service can treat the payload as the recipe's attributes and create
the new record (or another mutation) when appropriate:


.. code-block:: python

    from nautilus import Service, ServiceManager
    from nautilus.models import BaseModel, fields
    from nautilus.api.fields import Connection
    from nautilus.contrib.graphene_peewee import PeeweeObjectType
    from graphene import Schema

    class Recipe(HasId, BaseModel):
        name = fields.CharField()

    schema = Schema()

    @schema.register
    class RecipeObjectType(PeeweeObjectType):
        """ The GraphQL Object type for our recipes. """
        class Meta:
            model = Recipe

    class Query(graphene.ObjectType):
        """ the root level query for our recipe service """
        recipes = Connection(RecipeObjectType)

        def resolve_recipes(self, args, info):
            """ return all recipes in the database """
            return Recipe.query.all()

    # add the root query to the schema
    schema.query = Query


    def action_handler(action_type, payload):
        # if the payload represents a new recipe to create
        if action_type == 'create_recipe':
            # create a new instance of the recipe
            recipe = Recipe(**payload)
            # save the recipe instance
            recipe.save()


    class RecipeService(Service):
        schema = schema
        action_handler = action_handler

    manager = ServiceManager(RecipeService)

    if __name__ == '__main__':
        manager.run()

Feel free to test this by....

Congratulations! You have finally pieced together a complete nautilus service.
Now other entities in your cloud (like another service or even a javascript
client) can create, persist, and retrieve recipes without maintaining the data
themselves. In the next section you will learn how to create services based
off of pre-packages ones as well as keep track of a relationships between
different services in your cloud.
