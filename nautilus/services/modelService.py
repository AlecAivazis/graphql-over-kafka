# local imports
from nautilus.network import CRUDHandler, combineActionHandlers
from nautilus.api import create_model_schema
from nautilus.conventions.services import model_service_name
from nautilus.network.actionHandlers import noop_handler
from .service import Service

class ModelService(Service):
    """
        This service provides basic CRUD support as well as a schema for
        external consumption. Additional action handlers will be merged with
        internal ones.
    """

    def __init__(self, model, additonal_action_handler = noop_handler, **kwargs):
        # save a reference to the model this service is managing
        self.model = model

        # the schema to add to the service
        schema = create_model_schema(model)

        # the action handler is a combination
        action_handler = combineActionHandlers(
            # of the given one
            additonal_action_handler,
            # and a crud handler
            CRUDHandler(model)
        )

        name = kwargs.pop('name', None) or model_service_name(model)

        # create the service
        super().__init__(
            schema = schema,
            actionHandler = action_handler,
            name = name,
            **kwargs
        )
