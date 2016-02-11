# external imports
from flask import Blueprint, render_template, abort
from os import path
# local imports
from nautilus.auth import login_user, logout_user
from nautilus.network import query_graphql_service
from .forms import (
    LoginForm,
    RegistrationForm,
)


service_blueprint = Blueprint('auth', __name__, template_folder='templates')

@service_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    from .models import UserPassword

    form = LoginForm()

    # if we recieved a post request with valid information
    if form.validate_on_submit():
        # the form data
        data = form.data

        # get the user with matching email
        user = queryGraphQLService('http://localhost:8000', 'users', [
            'id',
            'firstName',
            'lastName',
            'email',
            'username',
        ], {
            'email': data['email']
        })[0]

        # look for a matching entry in the local database
        passwordEntry = UserPassword.query.filter_by(user=user['id']).first()

        # if the given password matches the stored hash
        if passwordEntry and passwordEntry.password == data['password']:
            # create a user object out of the remote user data
            user = User(**data)
            # log in the user
            login_user(user, remember=True)
            # redirect the user to the url parameter
            return redirect(request.args.get('next'))

        # otherwise the given password does not match the stored hash
        else:
            # add an error to the form
            flash('Sorry, that user/password combination was invalid.')

    # we did not recieve a post request with valid information
    return render_template('login.html', form=form)

@service_blueprint.route('/logout')
def logout():
    """
    Log a user out of their account.
    This view will log a user out of their account (destroying their session),
    then redirect the user to the home page of the site.
   """
    logout_user()
    return redirect('/')
