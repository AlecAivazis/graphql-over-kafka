from .decorators import *

from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
)

from .backend import init_app

def setupAuth(service):
    init_app(service.app)
