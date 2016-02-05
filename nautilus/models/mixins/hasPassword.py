# external imports
from sqlalchemy import Column
from sqlalchemy.orm import validates
# local imports
from ..types import Password

class HasPassword(object):
    password = Column(Password)

    # the decorate isn't necessary but ensures an immediate cast to a password hash and
    # prevents storing the raw password in memory. :thumbsup:
    @validates('password')
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)
