# external imports
import json
# local imports
from .kafka import KafkaBroker


class ActionHandler(KafkaBroker):

    consumer_channel = 'actions'
    producer_channel = 'actions'
    server = 'localhost:9092'


    async def handle_action(self, action_type, payload, props, **kwds):
        raise NotImplementedError()


    async def handle_message(self, **kwds):
        # call the user implemented function
        return await self.handle_action(**kwds)