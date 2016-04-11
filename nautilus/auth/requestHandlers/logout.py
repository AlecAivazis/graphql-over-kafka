# local imports
from .base import AuthRequestHandler

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
        return self.redirect(next_url)
