# external imports
import aiohttp_jinja2
# local imports
# from nautilus.network.util import query_service
from .base import AuthRequestHandler
from ..models import UserPassword
from .forms import LoginForm

class LoginHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        # render an empty login form to the view
        return dict(form=LoginForm())


    async def post(self):
        # the used responses
        from nautilus.network.http.responses import HTTPUnauthorized, HTTPFound
        # make sure we do anything important
        await super().post()
        # createa a form from the request parameters
        form = LoginForm(**self.request.arguments)
        # if we recieved valid information
        if form.validate():
            # the form data
            data = form.data
            # grab the given email
            supplied_email = data['email'][0].decode('utf-8')
            supplied_password = data['password'][0].decode('utf-8')

            # get the user with matching email
            user_data = query_service(
                service='user',
                fields=[
                    'id',
                    'email',
                ],
                filters={
                    'email': supplied_email
                }
            )[0]

            # look for a matching entry in the local database
            passwordEntry = UserPassword.select().where(
                UserPassword.user == user_data['id']
            )[0]

            # if the given password matches the stored hash
            if passwordEntry and passwordEntry.password == supplied_password:
                # grab the redirect url from the url arguments
                redirect_url = self.request.arguments.get('next', ['/'])[0]
                # redirect the user to the url parameter
                response = HTTPFound(location=redirect_url)
                # log in the user
                await self.login_user(user_data, response)
                # return the response
                return response

        # the username and password do not match
        return HTTPUnauthorized(
            body="Sorry, the username/password combination do not match."
        )