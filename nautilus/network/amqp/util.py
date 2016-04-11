"""
    This module defines various utilities for dealing with the network.
"""
def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combinedActionHandler(action_type, payload, dispatcher=None):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(action_type, payload, dispatcher=dispatcher)

    # return the combined action handler
    return combinedActionHandler
