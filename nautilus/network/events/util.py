"""
    This module defines various utilities for dealing with the network.
"""
from asyncio import iscoroutinefunction, iscoroutine

def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # make sure each of the given handlers is callable
    for handler in args:
        # if the handler is not a function
        if not (iscoroutinefunction(handler) or iscoroutine(handler)):
            # yell loudly
            raise ValueError("Provided handler is not a coroutine: %s" % handler)

    # the combined action handler
    async def combined_handler(dispatcher, action_type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            await handler(dispatcher, action_type, payload)

    # return the combined action handler
    return combined_handler
