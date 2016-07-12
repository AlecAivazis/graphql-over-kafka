# external imports
import aiohttp_jinja2
# local imports
# from nautilus.network.util import query_service
from .base import AuthRequestHandler
from ..models import UserPassword
from .forms import RegistrationForm

class RegisterHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    @aiohttp_jinja2.template('register.html')
    async def get(self):
        # render an empty login form to the view
        return dict(form=RegistrationForm())


    async def post(self):
        # the used responses
        from nautilus.network.http.responses import HTTPForbidden, HTTPFound

        # bubble up
        await super().post()

        form_args = {
            'email': self.request.GET['email'][0].decode('utf-8'),
            'password': self.request.GET['password'][0].decode('utf-8'),
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
                return HTTPForbidden(
                    body='Could not find corresponding user in remote service'
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

            # the response object
            response = HTTPFound(location=self.request.GET.get('next', '/'))
            # log in the user we just authorized
            await self.login_user(user_data, response)
            # move the user along
            return response

        # the username and password do not match
        return HTTPForbidden(
            body="Sorry, could not register that username/password."
        )