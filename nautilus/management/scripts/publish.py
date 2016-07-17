"""
    This command publishes a message to the event system for
    debugging perposes.
"""

# external imports
import click
import asyncio
import json
from aiokafka import AIOKafkaProducer

@click.option('--type', '-t', default='cli', help="The action type of the action to publish.")
@click.option('--payload', '-p', required=True, help="The payload of the message")
@click.command()
def publish(type, payload):
    """
        Publish a message with the specified action_type and payload over the
        event system. Useful for debugging.
    """
    async def _produce(loop):
        # the message payload
        message = json.dumps({
            'action_type': type,
            'payload': payload
        }).encode()

        # adds message to sending queue
        future = await producer.send('actions', message)
        # waiting for message to be delivered
        r = await future

        # notify the user
        print("Successfully published action to services.")

    # grab a reference to the current event loop
    loop = asyncio.get_event_loop()
    # create a producer
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers='localhost:9092')
    # run the production sequence
    loop.run_until_complete(producer.start())
    loop.run_until_complete(_produce(loop))
    loop.run_until_complete(producer.stop())
    # close the event loop
    loop.close()



