# third party imports
from flask.ext.login import UserMixin

class User(UserMixin):
    """ The base user class used by nautilus apps """

    def is_active(self):
        return self.status == 'ENABLED'
