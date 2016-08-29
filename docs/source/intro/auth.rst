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


Registration and Logging Users In
-----------------------------------

Along with queries and mutations corresponding to our remote services, the api
gateway also provides a few mutations for validating user credentials and
registering new users. In order to register a user, visit a running api gateway
and send the following query:

.. code-block:: text

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

.. code-block:: text

    mutation {
        loginUser(email:"foo", password:"bar") {
            user {
                id
            }
            sessionToken
        }
    }

Make sure to copy that ``sessionToken`` down somewhere. We'll use it to authenticate our
requests later on.


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


Providing Session Tokens to API Queries
----------------------------------------

In order to make an authenticated request to the API gateway, the request must contain
the session token in the ``Authentication`` header as a ``Bearer`` roken. For example,
say we logged in with a user and was given the session token ``foo``. Unfortunately,
graphiql does not allow the user to specify specific headers on requests. In order
to test authenticated route, we suggest you use a command utility like ``curl``:

.. code-block:: bash

    curl --header "Authentication: Bearer foo" localhost:8000
