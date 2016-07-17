Connecting Services Together
=============================

Given their highly specialized nature, a service is not very useful on its
own. So, let's add another to our example cloud. This is a good opportunity
to use some of the services that nautilus provides which are great starting
points when adding new functionalities to your cloud.


A second service to connect to
-------------------------------

Let's start by creating a new file called ``comments.py``
in our directory. Inside of this file, paste the following code:

.. code-block:: python

    # third party imports
    from nautilus import ModelService, ServiceManager
    # third party imports
    from nautilus.models import BaseModel, fields


    class Comment(BaseModel):
        contents = fields.CharField()

    class ServiceConfig:
        database_url = 'sqlite:///comments.db'

    class CommentService(ModelService):
        model = Comment
        config = ServiceConfig


    manager = ServiceManager(CommentService)

    if __name__ == '__main__':
        manager.run()




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
"many-to-many" because a recipe can have many ingredients and an ingredient can
be a member of many recipes (neither column is unique). Relationships can also be
classified as "one-to-one" and "one-to-many".

Make a new file called ``comments.py`` next to the previously created
files. Now, create a ConnectionService to manage the relationship between
recipes and ingredients:

.. code-block:: python

    # external imports
    from nautilus import ConnectionService

    class ServiceConfig:
        database_url = 'sqlite:///commentConnections.db'

    class Comments(ConnectionService):
        from_service = ('CatPhoto',)
        to_service = ('Comment',)

        config = ServiceConfig


Create the database for the two services and add some more dummy entries.
Make sure the two id's entered into the connection database correspond to actual
entries in the appropriate database. Again, you can run the service and check out
the various endpoints.

