# externals
import os
# local imports
from .decorators import *
from .primitives import *
from .models import *
from .util import *


root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'requestHandlers', 'templates')