"""
    This file is responsible for centralizing the service conventions used in nautilus.
"""

# local imports
from .models import get_model_string

def model_service_name(model):
    ''' the name of a service that manages a model '''
    return get_model_string(model)


def auth_service_name():
    return "auth"


def api_gateway_name():
    ''' the name of the default api gateway '''
    return "api"


def connection_service_name(*args):
    ''' the name of a service that manages the connection between services '''

    # the list of services to connect
    services = [service if isinstance(service, str) \
                        else get_model_string(service) for service in args]

    # combine the two names into the connection name
    return "{}_connection".format('_'.join(sorted(services)))
