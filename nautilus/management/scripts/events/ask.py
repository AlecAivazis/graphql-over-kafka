"""
    This command publishes a message to the event system for
    debugging perposes.
"""

# external imports
import click
import asyncio
# local imports
from nautilus.network.events.consumers import ActionHandler

@click.option('--type', '-t', default='cli', help="The action type of the action to publish.")
@click.option('--payload', '-p', required=True, help="The payload of the message")
@click.command()
def ask(type, payload):
    """
        Publish a message with the specified action_type and payload over the
        event system. Useful for debugging.
    """
    async def _produce():
        # notify the user that we were successful
        print("Dispatching action with type {}...".format(type))
        # fire an action with the given values
        response = await producer.ask(action_type=type, payload=payload)
        # show the user the reply
        print(response)

    # create a producer
    producer = ActionHandler()
    # start the producer
    producer.start()

    # get the current event loop
    loop = asyncio.get_event_loop()

    # run the production sequence
    loop.run_until_complete(_produce())

    # start the producer
    producer.stop()
