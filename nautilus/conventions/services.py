"""
    This file is responsible for centralizing the service conventions used in nautilus.
"""

# local imports
from .models import get_model_string

def model_service_name(model):
    ''' the name of a service that manages a model '''
    return get_model_string(model)

def connection_service_name(model1, model2):
    ''' the name of a service that manages the connection between two models '''
    # sort the names alphabetically
    [name1, name2] = sorted([get_model_string(model1), get_model_string(model2)])
    # combine the two names into the connection name
    return "{}_{}_connection".format(name1, name2)
