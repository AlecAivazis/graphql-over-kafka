Authentication
===============

Like usual, the bulk of our cloud's authentication logic lives within a
separate service. Let's begin by adding a new file to our directory
called ``auth.py`` with the following contents:

.. code-block:: python

    from nautilus import AuthService

    class ServiceConfig:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/passwords.db'

    service = AuthService(
        configObject = ServiceConfig
    )

This service provides basic user authentication and registration. When a user
interacts with a service like the API gateway or a client, they a bit of
information with every request that identifies them and indicates they are
logged in. If a service requires authentication and it cannot be found, the
user is redirected to this service to obtain such credentials. As such, this
service needs to only be responsible for maintaining user passwords. Other
bits of user information can be stored in another, less protected service.

Go ahead and run this service (remember to create the database). Navigate
to the ``/register`` endpoint and register an account for us to use. Log into
the account you just made by entering the same credentials into the ``/login``
endpoint.

Now we are ready to protect our data!


Authorizing Users for Particular Pieces of Data
------------------------------------------------

Regardless of your application, not all bits of information are inteded for
everyone to see. Eventually you'll want to be able to specify which users are
able to see which entries in our api. Thankfully, hiding pieces of data based
on the current user is easy in nautilus. Simply, add a function to your
``ServiceObjectType`` s called ``auth`` that takes the user as an argument and
returns true if the user can see the object and false if not. For example, say
we had set up a relationship between recipes and users through another
connection service. We could limit the results in the recipe query to only
those written by the current user by changing our recipe service object to
look something like:


.. code-block:: python

    class Recipe(ServiceObjectType):
        class Meta:
            service = RecipeService

        # assuming User was defined above/elsewhere
        author = Connection(User)

        def auth(self, user):
            """
                This function returns True if the given user is able to view
                this recipe.
            """
            return self.author.id == user.id
