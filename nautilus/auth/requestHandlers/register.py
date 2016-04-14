# external imports
import tornado
# local imports
from nautilus.network.util import query_service
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

            try:
                # get the user with matching email
                user_data = query_service(
                    service='user',
                    fields=[
                        'id',
                        'email',
                    ],
                    filters={
                        'email': data['email']
                    }
                )[0]
            # if there wasn't a matching user
            except IndexError:
                return self.finish(
                    'Could not find corresponding user in remote service'
                )

            # the query to find a matching query
            match_query = UserPassword.user == user_data['id']

            # if the user has already been registered
            if UserPassword.select().where(match_query).count() > 0:
                # yell loudly
                raise ValueError("The user is already registered.")
            # create an entry in the user password table
            password = UserPassword(user=user_data['id'], **data)
            # save it to the database
            password.save()

            # log in the user we just authorized
            self.login_user(user_data)

            # the url to redirect to when we're done
            redirect_url = self.request.arguments.get('next', '/')
            # move the user along
            return self.redirect(redirect_url)


        # the username and password do not match
        raise tornado.httputil.HTTPInputError(
            "Sorry, could not register that username/password."
        )

            # otherwise the given password does not match the stored hash
            # else:
                # add an error to the form
                # flash('Sorry, that user/password combination was invalid.')
