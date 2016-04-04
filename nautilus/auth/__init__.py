# externals
import random
import string
# local imports
from .decorators import *
from .primitives import *
from .forms import *
from .models import *
from .requestHandlers import *


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
