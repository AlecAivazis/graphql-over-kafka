# external imports
import json
import logging
# local imports
from . import BasicConsumer

LOGGER = logging.getLogger(__name__)


class ActionConsumer(BasicConsumer):
    """ This async consumer looks for messages in the action exchange and parses them as json """

    MESSAGE_URL = 'amqp://actions/'

    EXCHANGE = 'actions'
    EXCHANGE_TYPE = 'fanout'
    QUEUE = None # ensures the parent uses an automatically assigned name


    def __init__(self, actionHandler):
        # use the same url for all action consumers
        super().__init__(self.MESSAGE_URL)
        # save the handler
        self._actionHandler = actionHandler


    def on_message(self, channel, method, properties, body):
        """ Call the actionHandler when a message is recieved """
        # pass the message onto the parent class first
        super().on_message(channel, method, properties, body)
        # decode the body as a byte string
        bodyString = body.decode('utf-8')
        # parse the body as json
        bodyData = json.loads(bodyString)
        # if there is a type and payload
        if 'type' in bodyData and 'payload' in bodyData:
            # pass the type and payload to the action handler
            self._actionHandler(type = bodyData['type'], payload = bodyData['payload'])
        # otherwise its an invalid action
        else:
            LOGGER.warning('Encountered invalid action: {}'.format(bodyString) )
