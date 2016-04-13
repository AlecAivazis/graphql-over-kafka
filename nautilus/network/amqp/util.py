"""
    This module defines various utilities for dealing with the network.
"""
from collections.abc import Callable

def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combinedActionHandler(action_type, payload, dispatcher=None):
        # goes over every given handler
        for handler in args:
            # if the handler is not a function
            if not isinstance(handler, Callable):
                # yell loudly
                raise ValueError("Provided handler is not a function.")

            # call the handler
            handler(action_type, payload, dispatcher=dispatcher)

    # return the combined action handler
    return combinedActionHandler
