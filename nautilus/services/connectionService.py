# local imports
from nautilus.api import create_model_schema
from nautilus.network.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name
from .modelService import ModelService

class ConnectionService(ModelService):
    """
        This service manages a connection between any number of other services.
        The underlying schema and database are automatically generated to
        match the primary keys of the linked services.

        This service will listen for actions indicating the deletion of a related
        model and remove any related fields to maintain consistency. And provides
        a way for the api gateway to deduce the relationship between services when
        summarizing the cloud.

        Args:
            services (list of nautilus.Service): The list of services to connect.
            additonal_action_handler (optional, function): An action handler
                to be called alongside the internal ones.

        Example:

            .. code-block:: python

                # external imports
                from nautilus import ConnectionService

                # the services to connect
                from local.directory import service as service_one
                from other.local.directory import service as service_two

                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/connections.db'

                service = ConnectionService(
                    services = [service_one, service_two],
                    configObject = ServiceConfig
                )

    """

    def __init__(self, services, additonal_action_handler = noop_handler, **kwargs):

        # *sigh*
        from nautilus.models import create_connection_model

        # make sure we were passed more than one service
        if len(services) < 2:
            raise Exception("Please provide more than one service to connect")

        # # create the service
        super().__init__(
            model = create_connection_model(services),
            name = connection_service_name(*services),
            **kwargs
        )
