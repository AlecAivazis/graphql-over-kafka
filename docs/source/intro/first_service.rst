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

    service = Service(name='my service')

    if __name__ == '__main__':
        service.run()


You could also have wrapped your service in a ServiceManager
<nautilus.ServiceManager> which provides various command line arguments.
Feel free to test that this works by executing this script in your console:

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
that our service will manage. Nautilus uses SQLAlchemy for its internal
services and provides many helpers for common patterns. Therefore, while
not necessary, it is suggested that you also use SQLAlchemy to manage
your database. And honestly, it's one of the nicest python packages written,
so why not take the opportunity when you can?

Throughout this guide, we're going to be making a recipe list, so open up
server.py from the previous step and add the Recipe class.

.. code-block:: python

    from nautilus import Service, ServiceManager
    from nautilus.models import BaseModel, HasID
    from sqlalchemy import Column, Text

    # we're using the HasID mixin here to automatically provide a primary key
    # for the table
    class Recipe(HasId, BaseModel):
        name = Column(Text, description="The name of the recipe")

    service = Service(name='my service')

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()


Notice we also wrapped the service in a manager, which provides a basic
command line interface for our service.

While our service still can't talk to the outside world, at least it's keep
track of our recipes for us. By inheriting from BaseModel <nautilus.BaseModel>
nautilus automatically registers this model with an admin interface. But
before we can look at the records, we have to create the database that will
persist the data. Since our service is now wrapped in a manager, we can easily
do this by executing the ``syncdb`` command:

.. code-block:: bash

    $ python3 ./server.py syncdb

Now that you have a place to store your data, run the service and navigate your
browser to ``localhost:8000/admin``.You should see a button at the top which
will bring you to a page for directly managing the recipe instances. While this
is rather convinient for humans, we will need to add a way for other services
to query this database.


Building a Schema
-------------------

Traditionally, backend data is made availible via some sort of RESTful api. In
nautilus, services use a new technology called GraphQL from the facebook
engineers which allows the service to expose the data through a single
endpoint. For more information on GraphQL, visit this page.

Normally, building the description of our endpoint would result in a
significant amount of duplicated code (a new field for every model
attribute we want to include). However, recently the Graphene team added
automated support for SQLAlchemy models allowing us to add a graphql endpoint
to our service with a few additional lines:

.. code-block:: python

    from nautilus import Service, ServiceManager, db
    from nautilus.models import BaseModel, HasID
    from nautilus.api.fields import Connection
    from sqlalchemy import Column, Text
    from graphene import Schema
    from graphene.contrib.sqlalchemy import SQLAlchemyObjectType

    class Recipe(HasId, BaseModel):
        name = Column(Text, description="The name of the recipe")

    schema = Schema(session = db.session)

    @schema.register
    class RecipeObjectType(SQLAlchemyObjectType):
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

    service = Service(name='my service', schema = schema)

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()


Note: ``Connection`` is a very special type provided by nautilus.
For now, you can think of it as a wrapper around the List type that
we are using to make our code more easily read.

Sometimes, you might have to create the entire schema by hand, in which case
I suggest reading the graphene documentation [here](graphene). However, given
the simplicity of our Recipe model, Graphene can create the object for us.


Querying the Service's State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that our service has been given schema, we can query the internal state of
the service using two different endpoints. Nautilus uses GraphQL as the service
query langauge. Take a second to familiarize yourself with forming a GraphQL
query by reading [this]() short blog post.

If you navigate to the root url of your service (http://localhost:8000 by
default) you will see that the service  is trying to parse an incoming
query and can't find one. You can give the service a query to fulfill by
padding a value to the `query` url parameter by navigating to a url like
http://localhost:8000/?query={recipes{ name }}.

While this does work, it's clear this endpoint is not intended for human
consumption. Instead, if you point your browser to /graphiql you will
get visual environment for forming queries. I suggest opening a second tab
pointed at the admin interface previously discussed and proving to yourself
that the api is working as expected.


Responding to Actions
-----------------------

Now that our service maintains an internal state and can provide a summary of
that state to other services, all that's left is to provide a way for the
service to mutate its state as it recieves actions. To do this, we
just need to define a function that takes two parameters: ``type`` and
``payload``. ``Type`` identifies the event which allows the service to decide
if it needs to respond. ``Payload`` provides the associated data for the event.
For example, if an action means to indicate that a new recipe needs to be
created, the service can treat the payload as the recipe's attributes and
create the new record (or another mutation) when appropriate:


.. code-block:: python

    from nautilus import Service, ServiceManager, db
    from nautilus.models import BaseModel, HasID
    from nautilus.api.fields import Connection
    from sqlalchemy import Column, Text
    from graphene import Schema
    from graphene.contrib.sqlalchemy import SQLAlchemyObjectType

    class Recipe(HasId, BaseModel):
        name = Column(Text, description="The name of the recipe")

    schema = Schema(session = db.session)

    @schema.register
    class RecipeObjectType(SQLAlchemyObjectType):
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


    def action_handler(type, payload):
        # if the payload represents a new recipe to create
        if type == 'create_recipe':
            # create a new instance of the recipe
            recipe = Recipe(**payload)
            # save the recipe instance
            recipe.save()


    service = Service(
        name='my service',
        schema = schema,
        actionHandler = action_handler
    )

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()

Feel free to test this by....

Congratulations! You have finally pieced together a complete nautilus service.
Now other entities in your cloud (like another service or even a javascript
client) can create, persist, and retrieve recipes without maintaining the data
themselves. In the next section you will learn how to create services based
off of pre-packages ones as well as keep track of a relationships between
different services in your cloud.
