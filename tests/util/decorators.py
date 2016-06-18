# external imports
import asyncio
from unittest.mock import MagicMock
# local imports
from nautilus.network.events.consumers import KafkaBroker

loop = asyncio.get_event_loop()

def async_test(test_function):
    """
        This decorator wraps a test function and executes it on the asyncio
        event loop.
    """

    def function(*args, **kwds):

        # execute the test on the event loop
        handler = loop.run_until_complete(test_function(*args, **kwds))
        print(handler)
        # close the event loop
        loop.close()

    return function