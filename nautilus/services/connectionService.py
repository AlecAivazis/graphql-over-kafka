# local imports
from nautilus.network.events import combine_action_handlers
from nautilus.network.events.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name
from nautilus.conventions.actions import get_crud_action, success_status
from .modelService import ModelService
from nautilus.models.util import create_connection_model
from nautilus.conventions.api import service_node_name, connection_service_node_name


class ConnectionService(ModelService):
    """
        This service manages a "one-way" connection between two services.
        The underlying schema and database are automatically generated to
        match the primary keys of the linked services.

        This service will listen for actions indicating the deletion of a related
        model and remove any related fields to maintain consistency. And provides
        a way for the api gateway to deduce the relationship between services when
        summarizing the cloud.

        Args:
            services (list of nautilus.Service): The list of services to connect.

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
                    config = ServiceConfig

                    from_service = service_one
                    to_service = service_two

    """

    from_service = None
    to_service = None


    def __init__(self, **kwargs):

        # if there is no to service
        if not self.to_service:
            raise ValueError("Please provide a 'to_service'.")
        # if there is no to service
        if not self.from_service:
            raise ValueError("Please provide a 'from_service'.")

        # save a list of the models
        self._services = [self.to_service, self.from_service]
        # the models of each service
        self._service_models = [service.model for service in self._services]

        # make sure there is a unique name for every service
        if len({model.model_name for model in self._service_models}) \
               != len(self._service_models):
            raise ValueError("Can only connect models with different name")

        # create the service
        super().__init__(
            model=create_connection_model(self._service_models),
            name=connection_service_name(service=self),
            **kwargs
        )


    @property
    def action_handler(service):

        class ConnectionActionHandler(super().action_handler):
            async def handle_action(self, action_type, payload, **kwds):
                # a connection service should listen for deletes on linked services
                # connected_action_handlers = [self._create_linked_handler(model)
                #                              for model in self._service_models]

                # bubble up
                await super().handle_action(action_type, payload, **kwds)

                # for each model we care about
                for model in service._service_models:
                    # TODO: make this only happen once (not on every action)
                    # create the appropriate action handler
                    handler = service._create_linked_handler(model)
                    # call the handler
                    await handler(action_type, payload, **kwds)

        return ConnectionActionHandler


    @property
    def api_node_name(self):
        return connection_service_node_name(self)


    def summarize(self, **extra_fields):
        # start with the default summary
        try:
            return {
                **super().summarize(),
                'connection': {
                    'from': {
                        'service': self.from_service().api_node_name,
                    },
                    'to': {
                        'service': self.to_service().api_node_name,
                    }
                },
                **extra_fields
            }
        except Exception as e:
            print(e)


    def _create_linked_handler(self, model):
        # the related action type
        related_action_type = get_crud_action('delete', model, status=success_status())
        # the action handler
        async def action_handler(action_type, payload, notify=True, **kwds):
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
                ids = [model.id for model in self.model.filter(matching_records)]
                # find the matching records
                self.model.delete().where(matching_records).execute()

                # if we are supposed to notify
                if notify:
                    # notify of the related delete
                    await self.event_broker.send(
                        action_type=get_crud_action('delete', self.model, status=success_status()),
                        payload=ids
                    )


        # pass the action handler
        return action_handler



    def get_base_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return self._service_models
