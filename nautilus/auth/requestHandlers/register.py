# external imports
import aiohttp_jinja2
import json
# local imports
from nautilus.conventions.actions import get_crud_action
from nautilus.conventions.api import root_query
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
        from nautilus.network.http.responses import HTTPForbidden, HTTPFound, HTTPOk

        # bubble up
        await super().post()

        # grab the post data from the request
        post_data = await self.request.post()

        form_args = {
            'email': post_data['email'],
            'password': post_data['password'],
        }

        # create a form from the request parameters
        form = RegistrationForm(**form_args)

        # if we recieved a post request with valid information
        if form.validate():
            # the form data
            data = form.data

            # if there is a matching user
            if await self._check_for_matching_user(uid=post_data['email']):
                # that user has already been registered
                return HTTPForbidden(
                    body=b"Sorry, that user has already been registered."
                )

            # otherwise there is no matching user
            else:
                # so make one
                response_data = await self._create_remote_user(uid=post_data['email'])

                # the query to find a matching query
                match_query = UserPassword.user == response_data['id']

                # if the user has already been registered
                if UserPassword.select().where(match_query).count() > 0:
                    # yell loudly
                    raise ValueError("The user is already registered.")
                # create an entry in the user password table
                password = UserPassword(user=response_data['id'], **data)
                # save it to the database
                password.save()

                # the response object
                response = HTTPFound(location=self.request.GET.get('next', '/'))
                # log in the user we just authorized
                await self.login_user(response_data)
                # move the user along
                return response

        # the username and password do not match
        return HTTPForbidden(
            body="Sorry, could not register that username/password."
        )


    async def _check_for_matching_user(self, uid):
        """
            This function checks if there is a user with the same uid in the
            remote user service

            Args:
                uid (string): the identifier of the user to check for

            Returns:
                (bool): wether or not there is a matching user
        """
        # the action type for a remote query
        read_action = get_crud_action(method='read', model='user')
        # the query for matching entries
        payload = """
            query {
                %s(email: "%s") {
                    pk
                }
            }
        """ % (root_query(), uid)
        # perform the query
        user_data = json.loads(await self.service.event_broker.ask(
            action_type=read_action,
            payload=payload
        ))
        # there is a matching user if there are no errors and no results from
        # the remote query
        return not user_data['errors'] and len(user_data['data'][root_query()])


    async def _create_remote_user(self, uid):
        """
            This method creates a service record in the remote user service
            with the given email.

            Args:
                uid (str): the user identifier to create

            Returns:
                (dict): a summary of the user that was created
        """
        # the action for reading user entries
        read_action = get_crud_action(method='create', model='user')
        payload = {"email": uid}

        # see if there is a matching user
        user_data = await self.service.event_broker.ask(
            action_type=read_action,
            payload=payload
        )
        # treat the reply like a json object
        return json.loads(user_data)
