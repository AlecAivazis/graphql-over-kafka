Authentication
===============

Like usual, the bulk of our cloud's authentication logic lives within a
separate service. Let's begin by adding a new file to our directory
called ``auth.py`` with the following contents:

.. code-block:: python

    from nautilus import AuthService

    class ServiceConfig:
        database_url = 'sqlite:///passwords.db'

    class RecipeBookAuth(AuthService):
        config = ServiceConfig

We'll also need a service to maintain user information (like their e-mails). So
make a second file called ``user.py`` that resembles our other model services:

.. code-block:: python

    import nautilus
    from nautilus.models import BaseModel, fields

    class User(BaseModel):
        email = fields.CharField()

    class ServiceConfig:
        database_url = 'sqlite:///user.db'

    class UserService(nautilus.ModelService):
        model = User
        config = ServiceConfig


These services provide what's necessary for basic user authentication and
registration. When a user interacts with a service like the API gateway or a
client, they send a bit of information with every request that identifies
them and indicates they are logged in. Therefore, the auth service needs to only
be responsible for maintaining user passwords. Other bits of user information
are stored in the other, less protected service.

Go ahead and start both services (remember to create the databases). Navigate
to the ``/register`` endpoint of the auth service and register an account for
us to use. Log into the account you just made by entering the same credentials
into the ``/login`` endpoint.

Now we are ready to protect our data!


Authorizing Users for Particular Pieces of Data
------------------------------------------------

Regardless of your application, not all bits of information are inteded for
everyone to see. Eventually you'll want to be able to specify which users are
able to see which entries in our api. Thankfully, hiding pieces of data based
on the current user is easy in nautilus. Simply, add a function to the api
decorated to match the service record. This function takes the user as an argument
and returns true if the user can see the object and false if not. For example, say
we had set up a relationship between recipes and users through another
connection service. We could limit the results in the recipe query to only
those written by the current user by changing our api service to
look something like:

.. code-block:: python

    class API(nautilus.APIGateway):

        @nautilus.auth_criteria('CatPhoto')
        def auth_catPhoto(self, model, user):
            """
                This function returns True if the given user is able to view
                this photo.
            """
            return model.owner == user
