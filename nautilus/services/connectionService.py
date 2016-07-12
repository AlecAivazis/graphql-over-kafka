# local imports
from nautilus.network.events import combine_action_handlers
from nautilus.network.events.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name, model_service_name
from nautilus.conventions.actions import get_crud_action, success_status
from .modelService import ModelService
from nautilus.models.util import create_connection_model

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

                class ServiceConfig:
                    database_url = 'sqlite:////tmp/connections.db'

                class MyConnection(nautilus.ConnectionService):
                    config = ServiceConfig

                    from_service = ('service_one',)
                    to_service = ('service_one',)

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
        self._services = [self.to_service[0], self.from_service[0]]

        # make sure there is a unique name for every service
        if len(set(self._services)) != len(self._services):
            raise ValueError("Can only connect models with different name")

        # create the service
        super().__init__(
            model=create_connection_model(self),
            name=connection_service_name(self),
            **kwargs
        )


    @property
    def action_handler(self):
        # create a linked handler for every service
        linked_handlers = [self._create_linked_handler(service) \
                                        for service in self._services]

        class ConnectionActionHandler(super().action_handler):
            async def handle_action(self, *args, **kwds):
                """
                    a connection service should listen for deletes on linked services
                    as well as the usual model service behavior
                """

                # bubble up
                await super().handle_action(*args, **kwds)

                # for each service we care about
                for handler in linked_handlers:
                    # call the handler
                    await handler(*args, **kwds)

        return ConnectionActionHandler


    def summarize(self, **extra_fields):
        # start with the default summary
        try:
            return {
                **super().summarize(),
                'connection': {
                    'from': {
                        'service': model_service_name(self.from_service[0]),
                    },
                    'to': {
                        'service': model_service_name(self.to_service[0]),
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
                matching_records = getattr(self.model, model_service_name(model)) == related_id
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
