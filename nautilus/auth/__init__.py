# externals
import random
import string
# local imports
from .decorators import *
from .primitives import *
from .models import *
from .requestHandlers import *


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'requestHandlers', 'templates')