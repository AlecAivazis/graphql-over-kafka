Querying The Distributed Structure
===================================

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

.. code-block :: python

    # external imports
    from nautilus import APIGateway, ServiceManager

    class CatPhotoAPI(APIGateway): pass

    manager = ServiceManager(service)

    if __name__ == '__main__':
        manager.run()

When this service runs it sends an event that intstructs all other services to announce
their api contributitions. This information is pieced together to form a single api endpoint
that is used to query the entire system. With your CatPhoto service running, start up the api
passing a different port:

.. code-block :: bash

    python3 api.py runserver --port 8001

And visit the `/graphiql` endpoint like before. You should be able to see your other services
as queryable nodes in the api as well as some mutations to handle the internal
state of our model services.

Out of the box, nautilus provides a few filters for graphql nodes based on ModelServices, for
more information visit the `APIGateway Documentation <http://nautilus.github.io/nautilus/schema/index.html#filtering-the-api>`_.
