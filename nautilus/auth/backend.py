# external imports
from flask.ext.login import LoginManager
# local imports
from .primitives import User

# create a new login manager
loginManager = LoginManager()

# make sure unauthorized views are redirected to the auth service
loginManager.login_view = 'http://localhost:8005/login'

def config_app(app):
    """ set the necessary configuration parameters """
    app.config['REMEMBER_COOKIE_DOMAIN'] = '.syncatech.com'

@loginManager.user_loader
def load_user(user_id):
    """ loads the user by user id """
    return User(id=user_id)

def init_app(app):
    loginManager.init_app(app)
