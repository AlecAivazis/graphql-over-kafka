# from: http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy

# local imports
from nautilus.models import Field
from ...primitives import PasswordHash
# from nautilus.api import convert_sqlalchemy_type

class PasswordField(Field):
    """
        This field allows for safe storage of passwords in a database while
        supporting easy validation.

        Args:
            rounds (int, default=12): The number of layers of encryption to be
                performed on the hash. This value is upgradeable and can be
                increased at any time. The next time the value is updated, it
                will be saved with the increased encryption.

        Example:
            TODO: add example of equality test

    """
    db_field = 'varchar'

    def __init__(self, rounds=12, **kwds):
        self.rounds = rounds
        super().__init__(**kwds)


    def db_value(self, value):
        """
            This function is responsible for converting the python value
            to something that the databse knows how to handle - namely a string.
        """
        # make sure the given value is valid and then return the correspond hash
        return self._convert(value).hash


    def python_value(self, value):
        """
            This function returns the python object corresponding to the data
            left in the database.

            Convert the hash to a PasswordHash, if it's non-NULL.
        """
        if value is not None:
            return PasswordHash(value, rounds=self.rounds)


    def _convert(self, value):
        """
            This function is responsible for the actual conversion from a
            native type to a PasswordHash object.

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


# # Graphene Support

# @convert_sqlalchemy_type.register(PasswordField)
# def convert_column_to_string(type, column):
#     """ Make sure the password is never included in a schema. """
#     raise Exception("Passwords cannot be included in a schema. Make sure to explcitly ignore any password fields in models.")
