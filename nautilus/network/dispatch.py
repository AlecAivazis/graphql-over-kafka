""" Various helper functions for dealing with backend actions """

# external imports
import pika, json

def dispatch(body, exchange, routing_key = ''):
    """ dispatch the action through the message queue """
    # connect to the rabbit mq server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='actions'))
    # open a channel
    channel = connection.channel()
    # make sure the exchange matches our expectations
    channel.exchange_declare(exchange=exchange['name'], type=exchange['type'], durable=exchange['durable'])
    # send the message over the exchange
    channel.basic_publish(exchange=exchange['name'], routing_key=routing_key, body=body)
    # close the connection
    connection.close()

def dispatchAction(action):
    """ assume the dispatch text is a json object """
    # the exchange to dispatch to
    exchange = {
        'name': 'actions',
        'type': 'fanout',
        'durable': True,
    }
    # dispatch a stringified version of the action over the exchange
    dispatch(body = json.dumps(action), exchange = exchange)
