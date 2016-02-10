Hiding The Distributed Structure
=================================

We now have three different services which are each responsible for maintaining
a small bit of the application. While this has many benefits, one rather large
annoyance is the difficulty to create a summary of our application using data
that spans many services.

One way to solve this is to create a service known as an "API gateway" which,
unlike the services we have encountered so far, does not maintain any sort of
internal state. Instead, this service just has a single schema that describes
the entire cloud. This has a few major benefits that are worth pointing out:

* The distributed nature of the cloud is completely hidden behind a single endpoint
* Authorization is maintained by a single service
* Various network optimizations only need to occur in a single place
* The list of external mutations is in one place


Let's begin by creating a new file called ``api.py`` in our directory with the
following contents:

.. code-block:: python

    # external imports
    from nautilus import APIGateway, ServiceManager

    service = APIGateway()

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()


If you try to run this file as is, an exception will be thrown since we have
not provided the service with a schema that describes the complete topology of
our cloud.

Normally, supporting this schema involes bouncing a lot of different queries
between various ModelServices and their connections in order to create a single
report. This easily becomes very difficult to maintain, is prone to bugs,
and leads to a significant amount of code duplication (which is bad). While
not yet fully automated, nautilus makes the creation of this schema
significantly easier.

Rather than basing your schema object types on an SQLAlchemyObjectType like
before, services that you wish to use as representation for an external service
should be based on the SerivceObjectType. Add the following code blck at the
end of the api gateway file:

.. code-block:: python

    from graphene import String, ObjectType, Schema
    from nautilus.api import ServiceObjectType, Connection

    class Ingredient(ServiceObjectType):
        class Meta:
            service = 'ingredient'

        name = String(description = "The name of the ingredient.")


    class Recipe(ServiceObjectType):
        class Meta:
            service = 'recipe'

        name = String(description = "The name of the recipe.")


    class Query(ObjectType):
        ingredients = Connection(Ingredient)
        recipes = Connection(Recipes)

    schema = Schema()
    schema.query = Query


Notice the class Meta defined inside of the ServiceObjectType. The attribute
of the service parameter inside that class desingates the name of the service
to use as its source.

Remember earlier when you used a Connection and it acted just like a list?
Well, that's because the type you were connecting was a standard GraphQL one.
When the target of a connection is a service object, nautilus will use the
target's service keyword to look up the location of the service in the registry and
use its data. Go ahead and pass the schema to your service and give it a try.
You should be able to query the state of the recipe service from the api
service with a query like ``{ ingredients { name }}``. Pretty cool huh? Just
wait, it gets better.

Let's tell the API Gateway that there is a connection between ingredients
and recipes by adding a Connection field to the recipe class:

.. code-block:: python

    class Recipe(ServiceObjectType):
        class Meta:
            service = 'recipe'

        name = String(description = "The name of the recipe.")

        ingredients = Connection(
                        Ingredient,
                        description = "The ingredients in this recipe."
        )


When the a Connection is used between two ServiceObjects, nautilus will look up
the details of the relationship from the connection service we created earlier
and perform all of the necessary requests/joins to create the snapshot you
asked for.

You can test this out with a query like ``{ recipes {name, ingredients { name } } }``

Eventually all of this will be automated by taking advantage of GraphQL's
support for introspecting a schema without querying it.
