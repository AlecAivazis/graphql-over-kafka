# third party imports
from wtforms import Form
from wtforms.fields import PasswordField, StringField

# TODO: require values in both fields
class LoginForm(Form):
    """ Log in an existing user. """
    email = StringField('Login')
    password = PasswordField('Password')
