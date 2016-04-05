# local imports
from .service import Service
from nautilus.conventions.services import auth_service_name
from nautilus.auth.requestHandlers import (
    AuthRequestHandler,
    LoginHandler,
    LogoutHandler,
    RegisterHandler,
)

class AuthService(Service):
    """
        This service handles user authentication for the entire cloud and is
        the only service with access to the users passwords. As such, this
        service does not provide any sort of external schema, nor does it
        respond to actions by default. It's sole purpose is to collect the
        necessary information from the user and provide that user with a way
        to provid valid credentials to other services.

        Example:

            .. code-block:: python

                from nautilus import AuthService

                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/models.db'

                service = AuthService(
                    configObject = ServiceConfig,
                )
    """
    name = auth_service_name()

    @self.route('/login')
    class Login(LoginHandler): pass

    @self.route('/logout')
    class Logout(LogoutHandler): pass

    @self.route('/register')
    class Register(RegisterHandler): pass
