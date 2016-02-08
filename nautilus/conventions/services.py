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

    # figure out the model string
    model1_name = get_model_string(model1) if not isinstance(model1, str) else model1
    model2_name = get_model_string(model2) if not isinstance(model2, str) else model2

    # sort the names alphabetically
    [name1, name2] = sorted([model1_name, model2_name])

    # combine the two names into the connection name
    return "{}_{}_connection".format(name1, name2)
