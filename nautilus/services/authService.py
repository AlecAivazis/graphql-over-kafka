# local imports
from .service import Service
from nautilus.network.actionHandlers import noop_handler
from nautilus.auth.blueprints import service_blueprint
from nautilus.conventions.services import auth_service_name
from nautilus.auth.backend import loginManager

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

    def __init__(self, action_handler = noop_handler, **kwargs):

        # perform any necessary configuration first
        super().__init__(
            name = auth_service_name(),
            auth = False,
            **kwargs
        )

        # add the authentication blueprint to the service
        self.use_blueprint(service_blueprint)

        loginManager.init_app(self.app)


