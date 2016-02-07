"""
    This service maintains sensors registered with Synca.
"""

# local imports
from nautilus.network import CRUDHandler, combineActionHandlers
from nautilus.api import create_model_schema
from .service import Service

def noopHandler(type, payload):
    return

class ModelService(Service):
    """
        This service provides basic CRUD support as well as a schema for
        external consumption. Additional action handlers will be merged with
        internal ones.
    """

    def __init__(self, model, addtionalActionHandler = noopHandler, **kwargs):
        # the schema to add to the service
        schema = create_model_schema(model)
        # the action handler is a combination
        actionHandler = combineActionHandlers(
            addtionalActionHandler,
            CRUDHandler(model)
        )
        # create the service
        super().__init__(schema = schema, actionHandler = actionHandler, **kwargs)
