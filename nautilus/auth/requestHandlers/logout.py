# external imports
from tornado.web import redirect
# local imports
from .base import AuthRequestHandlerd

class LogoutHandler(AuthRequestHandler):
    """
        This class handles the basic login form.
    """

    def get(self):
        # log the current user out
        self.logout_user()
        # the next url for the user
        next_url = '/'
        # redirect the user to root
        return redirect(next_url)
