# external imports
import json
# local imports
from .actions import ActionHandler
from ..actionHandlers import query_handler, flexible_api_handler
from ..util import combine_action_handlers

class APIActionHandler(ActionHandler):
    """
        This action handler is used by the api service to build a schema
        of the underlying services as they announce their existence over
        the action system.
    """

    consumer_pattern = '(.*\..*\.(?!(pending)))|init|query'

    async def handle_action(self, *args, **kwds):

        # the combined handler
        handler = combine_action_handlers(
            # handle event-based queries
            # query_handler,
            # build the schema of possible services
            flexible_api_handler
        )

        # pass the arguments to the combination handler
        await handler(self.service, *args, **kwds)
