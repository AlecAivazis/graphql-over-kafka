# local imports
from .service import Service
import nautilus
from nautilus.conventions.services import auth_service_name
from nautilus.auth.requestHandlers import (
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

                import nautilus

                class ServiceConfig:
                    database_url = 'sqlite:////tmp/models.db'

                class MyAuth(nautilus.AuthService):
                    config = ServiceConfig
    """
    name = auth_service_name()

    def __init__(self, *args, **kwds):
        # bubble up
        super().__init__(*args, **kwds)
        # create the database
        self.init_db()


    def init_db(self):
        """
            This function configures the database used for models to make
            the configuration parameters.
        """
        # get the database url from the configuration
        db_url = self.config.get('database_url', 'sqlite:///nautilus.db')
        # configure the nautilus database to the url
        nautilus.database.init_db(db_url)


    def get_models(self):
        return [nautilus.auth.models.UserPassword]


@AuthService.route('/login')
class Login(LoginHandler): pass

@AuthService.route('/logout')
class Logout(LogoutHandler): pass

@AuthService.route('/register')
class Register(RegisterHandler): pass
