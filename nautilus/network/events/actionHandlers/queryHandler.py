# local imports
from nautilus.conventions.actions import query_action_type

def query_handler(service, action_type, payload, props, **kwds):
    """
        This action handler interprets the payload as a query to be executed
        by the api.
    """
    # check that the action type indicates a query
    if action_type == query_action_type():
        pass