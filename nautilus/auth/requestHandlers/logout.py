# local imports
from .base import AuthRequestHandler

class LogoutHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    async def get(self):
        # the used responses
        from nautilus.network.http.responses import HTTPFound
        # the response object
        response = HTTPFound(location='/')
        print(await self.get_current_user())
        # log the current user out
        await self.logout_user(response)
        # redirect the user to root
        return response
