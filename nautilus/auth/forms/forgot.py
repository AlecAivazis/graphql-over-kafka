# third party imports
from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class ForgotPasswordForm(Form):
    """
    Retrieve a user's email address for initializing the password reset
    workflow.
    This class is used to retrieve a user's email address.
    """
    email = StringField('Email', validators=[InputRequired()])
