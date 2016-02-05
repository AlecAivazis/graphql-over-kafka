# external imports
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
)
# local imports
from .decorators import *
from .backend import init_app
from .primitives import *

def init_service(service):
    init_app(service.app)
