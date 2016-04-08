# external imports
import tornado
# local imports
from nautilus.network.util import query_service
from nautilus.conventions.services import api_gateway_name
from .base import AuthRequestHandler
from ..models import UserPassword
from .forms import RegistrationForm

class RegisterHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    def get(self):
        # render an empty login form to the view
        return self.render('templates/register.html', form=RegistrationForm())


    def post(self):
        form_args = {
            'email': self.request.arguments['email'][0].decode('utf-8'),
            'password': self.request.arguments['password'][0].decode('utf-8'),
        }

        # create a form from the request parameters
        form = RegistrationForm(**form_args)

        # if we recieved a post request with valid information
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

            # create an entry in the user password table
            password = UserPassword(**data, user=user_data['id'])
            # save it to the database
            password.save()

            # move the user along
            return self.redirect(request.args.get('next'))


        # the username and password do not match
        raise tornado.httputil.HTTPInputError(
            "Sorry, could not register that username/password."
        )

            # otherwise the given password does not match the stored hash
            # else:
                # add an error to the form
                # flash('Sorry, that user/password combination was invalid.')
