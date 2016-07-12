"""
    This module defines various utilities for dealing with the network.
"""
from asyncio import iscoroutinefunction, iscoroutine

def combine_action_handlers(*handlers):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # make sure each of the given handlers is callable
    for handler in handlers:
        # if the handler is not a function
        if not (iscoroutinefunction(handler) or iscoroutine(handler)):
            # yell loudly
            raise ValueError("Provided handler is not a coroutine: %s" % handler)

    # the combined action handler
    async def combined_handler(*args, **kwds):
        # goes over every given handler
        for handler in handlers:
            # call the handler
            await handler(*args, **kwds)

    # return the combined action handler
    return combined_handler
