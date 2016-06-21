"""
    This file is responsible for centralizing the action conventions used in nautilus.
"""

# local imports
from .models import get_model_string


def get_crud_action(method, model, status='pending'):
    return "%s.%s.%s" % (method, get_model_string(model), status)


def change_action_status(action_type, new_status):
    """
        This function changes the status of an action type.
    """
    # replace the last bit of a dot separate string with the new_status
    return "%s.%s" % ('.'.join(action_type.split('.')[:-1]) , new_status)


def intialize_service_action(service=None, **kwds):
    # get the name of the service
    name = service.name if service else '*'
    # treat initialization like a crud action for services
    return get_crud_action('init', name, **kwds)