""" Various helper functions for dealing with backend actions """

# external imports
import pika, json

def dispatch(body, exchange, routing_key=''):
    """ dispatch the action through the message queue """
    # connect to the rabbit mq server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # open a channel
    channel = connection.channel()
    # make sure the exchange matches our expectations
    channel.exchange_declare(
        exchange=exchange['name'],
        type=exchange['type'],
        durable=exchange['durable']
    )
    # send the message over the exchange
    channel.basic_publish(exchange=exchange['name'], routing_key=routing_key, body=body)
    # close the connection
    connection.close()


def dispatch_action(action_type, payload):
    """
        This function dispatches an event over the action exchange with the designated
        type and payload.

        Args:
            action_type (string): The type of the action. Used by action handlers to figure out
                if it should respond to the event.
            payload (anything serializable): The payload associated with the action.
    """
    # the exchange to dispatch to
    exchange = {
        'name': 'actions',
        'type': 'fanout',
        'durable': True,
    }

    # the action object
    action = {
        'type': action_type,
        'payload': payload,
    }

    # dispatch a stringified version of the action over the exchange
    dispatch(body=json.dumps(action), exchange=exchange)
