

def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combinedActionHandler(action_type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(action_type, payload)

    # return the combined action handler
    return combinedActionHandler
