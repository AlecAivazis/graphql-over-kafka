# external imports
from flask.ext.login import UserMixin

class User(UserMixin):
    """ The base user class used by nautilus apps """

    def __init__(self, **kwargs):
        # loop over the given kwargs
        for key, value in kwargs.items():
            # treat them like attribute assignments
            setattr(self, key, value)
