# external imports
from flask import Blueprint, render_template, abort, redirect, request, flash
from os import path
# local imports
from nautilus.auth import login_user, logout_user
from nautilus.network import query_graphql_service
from .forms import (
    LoginForm,
    RegistrationForm,
)
from .models import UserPassword
from .primitives import User


service_blueprint = Blueprint('auth', __name__, template_folder='templates')

@service_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    # if we recieved a post request with valid information
    if form.validate_on_submit():
        # the form data
        data = form.data

        # get the user with matching email
        user_data = query_graphql_service('http://localhost:8000', 'users', [
            'id',
            'email',
        ], {
            'email': data['email']
        })[0]

        # look for a matching entry in the local database
        passwordEntry = UserPassword.query.filter(UserPassword.user == user_data['id']).first()

        # if the given password matches the stored hash
        if passwordEntry and passwordEntry.password == data['password']:
            # create a user object out of the remote user data
            user = User(**user_data)
            print(user)
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

@service_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    # if we recieved a post request with valid information
    if form.validate_on_submit():
        # the form data
        data = form.data

        # create an entry in the user password table
        password = UserPassword(**data)
        # save it to the database
        password.save()

        # move the user along
        return redirect(request.args.get('next'))

    # we did not recieve a post request with valid information
    return render_template('register.html', form=form)
