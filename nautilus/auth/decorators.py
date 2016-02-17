from flask import request, abort
from flask.ext.login import login_required as flask_login_required
from flask.ext.login import current_user, login_url
from functools import wraps

# A set of HTTP methods which are exempt from `login_required`.
# By default, this is just ``OPTIONS``.
EXEMPT_METHODS = set(['OPTIONS'])

def login_required(func):
    '''
        Decorating a view with this will ensure that the current user is
        logged in and authentication before calling the view. If a user
        is not logged in, they are redirected to the auth service to provide
        the necessary credentials.

        Example:

            @service.app.route('/foo)
            @login_required
            def hello():
                return 'world'
    '''

    def forward_to_login():

        try:
            # find the auth service location
            login_endpoint = 'http://' + service_location_by_name(auth_service_name())
            # redirect the user to the endpoint with a way to redirect them back
            return redirect(login_url(login_endpoint, request.url))

        # if the auth service does not exist
        except:
            # send an unauthorized error code
            abort(401)

    @wraps(func)
    def decorated_view(*args, **kwargs):
        # if the request cannot be authenticated
        if request.method in EXEMPT_METHODS:
            # pass the view along
            return func(*args, **kwargs)
        # if login is disabled
        elif current_app.login_manager._login_disabled:
            # pass the view along
            return func(*args, **kwargs)
        # if the current user isn't authenticated
        elif not current_user.is_authenticated:
            # send the user to the auth
            return forward_to_login()
        return func(*args, **kwargs)

    # return the decorated view
    return decorated_view

