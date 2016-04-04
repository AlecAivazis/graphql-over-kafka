from .base import AuthRequestHandler
from .login import LoginHandler
from .logout import LogoutHandler
from .register import RegisterHandler

root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')
static_dir = os.path.join(root_dir, 'static', 'build')
