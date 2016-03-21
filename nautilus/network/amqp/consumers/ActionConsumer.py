# external imports
import json
import logging
# local imports
from . import BasicConsumer

LOGGER = logging.getLogger(__name__)


class ActionConsumer(BasicConsumer):
    """ This async consumer looks for messages in the action exchange and parses them as json """

    MESSAGE_URL = 'amqp://localhost/'

    EXCHANGE = 'actions'
    EXCHANGE_TYPE = 'fanout'
    QUEUE = None # ensures the parent uses an automatically assigned name


    def __init__(self, action_handler):
        # use the same url for all action consumers
        super().__init__(self.MESSAGE_URL)
        # save the handler
        self._action_handler = action_handler


    def on_message(self, channel, method, properties, body):
        """ Call the actionHandler when a message is recieved """
        # pass the message onto the parent class first
        super().on_message(channel, method, properties, body)
        # decode the body as a byte string
        body_string = body.decode('utf-8')
        # parse the body as json
        body_data = json.loads(body_string)
        # if there is a type and payload
        if 'type' in body_data and 'payload' in body_data:
            # pass the type and payload to the action handler
            self._action_handler(action_type=body_data['type'], payload=body_data['payload'])
        # otherwise its an invalid action
        else:
            LOGGER.warning('Encountered invalid action: {}'.format(body_string))
