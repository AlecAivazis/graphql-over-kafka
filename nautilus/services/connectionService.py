# local imports
from nautilus.network import CRUDHandler, combineActionHandlers
from nautilus.api import create_model_schema
from nautilus.network.actionHandlers import noop_handler
from nautilus.conventions.services import connection_service_name
from .modelService import ModelService

class ConnectionService(ModelService):
    """
        This service provides basic CRUD functionality around the connection
        between two other services. Additional action handlers will be merged with
        internal ones.
    """

    def __init__(self, services = [], additonal_action_handler = noop_handler, **kwargs):

        # *sigh*
        from nautilus.models import create_connection_model

        # make sure we were passed more than one service
        if len(services) < 2:
            raise Exception("Please provide more than one service to connect")

        # # create the service
        super().__init__(
            # schema = create_model_schema(model),
            model = create_connection_model(services),
            name = connection_service_name(*services),
            **kwargs
        )
