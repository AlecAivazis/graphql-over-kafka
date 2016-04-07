# external imports
import tornado
# local imports
from nautilus.network import query_service
from nautilus.conventions.services import api_gateway_name
from .base import AuthRequestHandler
from ..models import UserPassword
from .forms import (
    LoginForm,
    RegistrationForm,
)

class LoginHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    def get(self):
        # render an empty login form to the view
        return self.render('templates/login.html', form=LoginForm())


    def post(self):
        # createa a form from the request parameters
        form = LoginForm(self.arguments)
        # if we recieved valid information
        if form.validate():
            # the form data
            data = form.data

            # get the user with matching email
            user_data = query_service(api_gateway_name(), 'users', [
                'id',
                'email',
            ], {
                'email': data['email']
            })[0]

            # look for a matching entry in the local database
            passwordEntry = UserPassword.select().where(
                UserPassword.user == user_data['id']
            )[0]

            # if the given password matches the stored hash
            if passwordEntry and passwordEntry.password == data['password']:
                # create a user object out of the remote user data
                user = User(**user_data)
                # log in the user
                self.login_user(user)
                # redirect the user to the url parameter
                return self.redirect(request.args.get('next'))

        # the username and password do not match
        raise tornado.httputil.HTTPInputError(
            "Sorry, the username/password combination do not match."
        )

            # otherwise the given password does not match the stored hash
            # else:
                # add an error to the form
                # flash('Sorry, that user/password combination was invalid.')
