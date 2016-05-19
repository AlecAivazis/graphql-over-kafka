"""
    This module defines various utilities for dealing with the network.
"""
from collections.abc import Callable

def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # make sure each of the given handlers is callable
    for handler in args:
        # if the handler is not a function
        if not isinstance(handler, Callable):
            # yell loudly
            raise ValueError("Provided handler is not a function: " + handler)

    # the combined action handler
    def combined_handler(dispatcher, action_type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(dispatcher, action_type, payload)

    # return the combined action handler
    return combined_handler
