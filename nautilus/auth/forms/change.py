# third party imports
from wtforms import Form
from wtforms.fields import PasswordField
from wtforms.validators import InputRequired, ValidationError

class ChangePasswordForm(Form):
    """
        Change a user's password.
        This class is used to retrieve a user's password twice to ensure it's valid
        before making a change.
    """
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    password_again = PasswordField(
        'Password (again)',
        validators=[InputRequired()]
    )

    def validate_password_again(self, field):
        """
        Ensure both password fields match, otherwise raise a ValidationError.
        :raises: ValidationError if passwords don't match.
        """
        if self.password.data != field.data:
            raise ValidationError("Passwords don't match.")
