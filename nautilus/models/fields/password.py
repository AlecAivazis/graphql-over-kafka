# from: http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy

# external imports
from sqlalchemy import Text, TypeDecorator
# local imports
from nautilus.auth.primitives import PasswordHash
from nautilus.api import convert_sqlalchemy_type

class PasswordField(TypeDecorator):
    """Allows storing and retrieving password hashes using PasswordHash."""
    impl = Text

    def __init__(self, rounds=12, **kwds):
        self.rounds = rounds
        super(Password, self).__init__(**kwds)

    def process_bind_param(self, value, dialect):
        """Ensure the value is a PasswordHash and then return its hash."""
        return self._convert(value).hash

    def process_result_value(self, value, dialect):
        """Convert the hash to a PasswordHash, if it's non-NULL."""
        if value is not None:
            return PasswordHash(value, rounds=self.rounds)

    def validator(self, password):
        """Provides a validator/converter for @validates usage."""
        return self._convert(password)

    def _convert(self, value):
        """Returns a PasswordHash from the given string.

        PasswordHash instances or None values will return unchanged.
        Strings will be hashed and the resulting PasswordHash returned.
        Any other input will result in a TypeError.
        """
        # if the value is already a password hash
        if isinstance(value, PasswordHash):
            # then don't do anything
            return value
        # or if the value is a string
        elif isinstance(value, str):
            # convert it to a password hash
            return PasswordHash.new(value, self.rounds)
        # otherwise the value is something we can't convert
        elif value is not None:
            # fail loudly
            raise TypeError(
                'Cannot convert {} to a PasswordHash'.format(type(value)))


# Graphene Support

@convert_sqlalchemy_type.register(Password)
def convert_column_to_string(type, column):
    """ Make sure the password is never included in a schema. """
    raise Exception("Passwords cannot be included in a schema. Make sure to explcitly ignore any password fields in models.")
