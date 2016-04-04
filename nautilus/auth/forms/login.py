# third party imports
from wtforms import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired

class LoginForm(Form):
    """ Log in an existing user. """
    email = StringField('Login', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
