Authentication
===============

Before we begin restricting bits of our api to particular users, we  need a service to
maintain user information (like their e-mails). So make a second file called ``user.py``
that resembles our other model services:

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


Validating / Providing Credentials
-----------------------------------

Along with queries and mutations corresponding to our remote services, the api
gateway also provides a few mutations for validating user credentials and
registering new users. In order to register a user, visit a running api gateway
and send the following query:

.. code-block::

    mutation {
        registerUser(email:"foo", password:"bar") {
            user {
                id
            }
            sessionToken
        }
    }

Assuming the user information is valid, the gateway should reply with the requested
information of the new user as well as a token that reqeusts that require authentication
provide.

The next time the user tries to access your application, they will probably need to
provide their credentials a second time. In order to validate those, the api
gateway provides another mutation for logging users in:

..code-block::

    mutation {
        loginUser(email:"foo", password:"bar") {
            user {
                id
            }
            sessionToken
        }
    }

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
connection service with a relationship named "owner". We could limit the results
in the recipe query to only those written by the current user by changing our api
service to look something like:

.. code-block:: python

    class API(nautilus.APIGateway):

        @nautilus.auth_criteria('catPhoto')
        async def auth_catPhoto(self, model, user_id):
            """
                This function returns True if the given user is able to view
                this photo.
            """
            return await model.owner._has_id(user_id)
