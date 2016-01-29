""" Various helper functions for dealing with backend actions """

# imports
from datetime import datetime, timedelta
import pika, os, json
from time import sleep

# messaging queue constants
server = 'actions'
exchange = 'actions'

def dispatch(action):
    """ dispatch the action through the message queue """
    # connect to the rabbit mq server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, type="fanout", durable=True)

    channel.basic_publish(exchange=exchange,
                          routing_key='',
                          body=json.dumps(action))

    connection.close()



def listenForActions(callback):
    """ listen for events in the message queue and call the handler after decoding """
    # the time we started the command (to later timeout)
    startTime = datetime.now()

    while True:
        # if more than 10 seconds have passed
        if datetime.now() - startTime > timedelta(seconds=10):
            print("rabbitMQ timed out")
            return

        # attempt to
        try:
            # connect to the message queue
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
        # if it failed
        except pika.exceptions.ConnectionClosed as error:
            # wait a bit
            sleep(0.1)
        # if it succeeds
        else:
            print('connected!')
            # leave the loop
            break

    # establish a channel
    channel = connection.channel()
    # make sure the actions channel exists
    channel.exchange_declare(exchange=exchange, type='fanout', durable=True)

    # create an exclusive queue for this service
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # connect the queue to the exchange
    channel.queue_bind(exchange=exchange, queue=queue_name)

    # called when a message comes over the queue
    def action_callback(ch, method, properties, body):
        # perform the specific action for the event
        callback(json.loads(body.decode('utf-8')))

    # start listening to the exchange
    channel.basic_consume(action_callback, queue=queue_name, no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
