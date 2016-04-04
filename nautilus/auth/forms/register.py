# third party imports
from wtforms import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired


class RegistrationForm(Form):
    """  Register a new user.  """
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
