Auth
=====

This page summarizes points on authentication in nautilus apart from the basic
workflow outlined in the `getting started guide <../intro/auth.html>`_.

Customizing User Session
-------------------------

Customizing the information stored in a user session (and therefore the criteria)
by which you can authorize the user is easy. Simply define a method in your api
gateway called ``user_session`` which takes the remote record of the user and
returns a dictionary with that users sesstion:

..code-block:: python

class MyAPI(nautilus.APIGateway):

    def user_session(user):
        return {
            'id': user['id'],
            'name': user['name']
        }
