# third party imports
from flask.ext.wtf import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, ValidationError


class RegistrationForm(Form):
    """  Register a new user.  """
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class LoginForm(Form):
    """ Log in an existing user. """
    email = StringField('Login', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class ForgotPasswordForm(Form):
    """
    Retrieve a user's email address for initializing the password reset
    workflow.
    This class is used to retrieve a user's email address.
    """
    email = StringField('Email', validators=[InputRequired()])


class ChangePasswordForm(Form):
    """
    Change a user's password.
    This class is used to retrieve a user's password twice to ensure it's valid
    before making a change.
    """
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Password (again)', validators=[InputRequired()])

    def validate_password_again(self, field):
        """
        Ensure both password fields match, otherwise raise a ValidationError.
        :raises: ValidationError if passwords don't match.
        """
        if self.password.data != field.data:
            raise ValidationError("Passwords don't match.")
