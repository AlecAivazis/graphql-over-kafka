# external imports
import aiohttp_jinja2
import json
# local imports
from nautilus.conventions.api import root_query
from nautilus.conventions.actions import get_crud_action
from .base import AuthRequestHandler
from .forms import LoginForm
from ..models import UserPassword

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

        # grab the post data from the request
        post_data = await self.request.post()
        # createa a form from the request parameters
        form = LoginForm(**post_data)

        # if we recieved valid information
        if form.validate():
            # the form data
            data = form.data
            # grab the given email
            supplied_email = data['email']
            supplied_password = data['password']

            # find the matching user with the given email
            user_data = await self._get_matching_user(supplied_email)

            # look for a matching entry in the local database
            passwordEntry = UserPassword.select().where(
                UserPassword.user == user_data['id']
            )[0]

            # if the given password matches the stored hash
            if passwordEntry and passwordEntry.password == supplied_password:
                # grab the redirect url from the url arguments
                redirect_url = self.request.GET.get('next', '/')
                # redirect the user to the url parameter
                response = HTTPFound(location=redirect_url)
                # log in the user
                await self.login_user(user_data)
                # return the response
                return response

        # the username and password do not match
        return HTTPUnauthorized(
            body="Sorry, the username/password combination do not match."
        )


    async def _get_matching_user(self, uid):
        # the action type for a remote query
        read_action = get_crud_action(method='read', model='user')
        # the query for matching entries
        payload = """
            query {
                %s(email: "%s") {
                    id
                    email
                }
            }
        """ % (root_query(), uid)

        # perform the query
        user_data = json.loads(await self.service.event_broker.ask(
            action_type=read_action,
            payload=payload
        ))

        # if there are errors or no matching user
        if user_data['errors'] or len(user_data['data'][root_query()]) != 1:
            # yell loudly
            raise ValueError("Could not find matching user")
        # otherwise there was a matching user
        else:
            # return the matching user record
            return user_data['data'][root_query()][0]
