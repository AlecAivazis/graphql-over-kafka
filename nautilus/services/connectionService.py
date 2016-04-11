# local imports
from nautilus.api import create_model_schema
from nautilus.network.amqp.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name
from .modelService import ModelService
from nautilus.models.util import create_connection_model

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
                import nautilus

                # the services to connect
                from local.directory import service as service_one
                from other.local.directory import service as service_two

                class ServiceConfig:
                    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/connections.db'

                class MyConnection(nautilus.ConnectionService):
                    services = [service_one, service_two]
                    config = ServiceConfig

    """

    services = []
    additional_action_handler = noop_handler

    def __init__(self, **kwargs):

        # make sure we were passed more than one service
        if len(self.services) < 2:
            raise ValueError("Please provide more than one service to connect.")

        # the models of each service
        self._service_models = [service.model for service in self.services]

        # make sure there is a unique name for every service
        if len({model.model_name for model in self._service_models}) \
               != len(self._service_models):
            raise ValueError("Can only connect models with different name")

        # create the service
        super().__init__(
            model=create_connection_model(self._service_models),
            name=connection_service_name(*self.services),
            **kwargs
        )


    def get_base_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return self._service_models
