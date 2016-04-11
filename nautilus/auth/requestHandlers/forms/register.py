# third party imports
from wtforms import Form
from wtforms.fields import PasswordField, StringField

# TODO: require values in both fields
class RegistrationForm(Form):
    """  Register a new user.  """
    email = StringField('Email')
    password = PasswordField('Password')
