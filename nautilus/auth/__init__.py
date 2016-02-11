# external imports
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
)
import random
import string
# local imports
from .decorators import *
from .backend import init_app
from .primitives import *
from .forms import *

def init_service(service):
    init_app(service.app)

def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
