# external imports
import json
# local imports
from .kafka import KafkaBroker


class ActionHandler(KafkaBroker):

    consumer_channel = 'actions'
    producer_channel = 'actions'
    server = 'localhost:9092'


    async def handle_action(self, action_type, payload):
        raise NotImplementedError()


    async def handle_message(self, msg, props):
        # parse the msg as json
        message = json.loads(msg)
        # call the user implemented function
        return await self.handle_action(
            action_type=message['type'],
            payload=message['payload']
        )