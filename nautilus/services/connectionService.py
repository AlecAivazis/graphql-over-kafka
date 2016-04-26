# local imports
from nautilus.api import create_model_schema
from nautilus.network.amqp import combine_action_handlers
from nautilus.network.amqp.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name
from nautilus.conventions.actions import get_crud_action
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
                    database_url = 'sqlite:////tmp/connections.db'

                class MyConnection(nautilus.ConnectionService):
                    services = [service_one, service_two]
                    config = ServiceConfig

    """

    services = []


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
            name=connection_service_name(*self._service_models),
            **kwargs
        )


    @property
    def action_handler(self):
        # a connection service should listen for deletes on linked services
        connected_action_handlers = [self._create_linked_handler(model)
                                     for model in self._service_models]

        # mix the related action handlers into supers
        return combine_action_handlers(
            super().action_handler,
            *connected_action_handlers
        )


    def _create_linked_handler(self, model):
        # the related action type
        related_action_type = get_crud_action('delete', model, status='success')
        # the action handler
        def action_handler(action_type, payload, dispatcher):
            """
                an action handler to remove related entries in the
                connection db.
            """
            # if the action designates a successful delete of the model
            if action_type == related_action_type:
                # the id of the deleted model
                related_id = payload['id']
                # the query for matching fields
                matching_records = getattr(self.model, model.model_name.lower()) == related_id
                # find the matching records
                self.model.delete().where(matching_records).execute()


        # pass the action handler
        return action_handler



    def get_base_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return self._service_models
