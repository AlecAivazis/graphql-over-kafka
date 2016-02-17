# external imports
from flask.ext.login import LoginManager
# local imports
from .primitives import User
from nautilus.network.registry import service_location_by_name
from nautilus.conventions.services import auth_service_name

# create a new login manager
loginManager = LoginManager()


def config_app(app):
    """ set the necessary configuration parameters """
    app.config['REMEMBER_COOKIE_DOMAIN'] = '.syncatech.com'

@loginManager.user_loader
def load_user(user_id):
    """ loads the user by user id """
    return User(id=user_id)

def init_app(app):
    loginManager.init_app(app)
