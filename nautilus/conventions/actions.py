"""
    This file is responsible for centralizing the action conventions used in nautilus.
"""
# external imports
import json
# local imports
from .models import get_model_string


def get_crud_action(method, model, status='pending', **kwds):
    return "%s.%s.%s" % (method, get_model_string(model), status)


def change_action_status(action_type, new_status):
    """
        This function changes the status of an action type.
    """
    # replace the last bit of a dot separate string with the new_status
    return "%s.%s" % ('.'.join(action_type.split('.')[:-1]) , new_status)


def roll_call_type():
    return "roll_call"


# TODO: check that it the args actually implement Serializable
def serialize_action(action_type, payload, **extra_fields):
    """
        This function returns the conventional form of the actions.
    """
    action_dict =  dict(
        action_type=action_type,
        payload=payload,
        **extra_fields
    )
    # return a serializable version
    return json.dumps(action_dict)


def hydrate_action(serialized):
    """
        This function takes a serialized action and provides the primitive
        data structure.
    """
    try:
        return json.loads(serialized)
    except:
        return {
            'action_type': 'unknown',
            'payload': str(serialized)
        }

def query_action_type():
    """
        This action type corresponds to an api query performed over the event system
    """
    return get_crud_action(model='api', method='query')


def intialize_service_action(all_services=False, **kwds):
    # get the name of the service
    name = 'service' if not all_services else '*'
    # treat initialization like a crud action for services
    return get_crud_action('init', name, **kwds)


def success_status():
    return 'success'


def error_status():
    return 'error'


def pending_status():
    return 'pending'
