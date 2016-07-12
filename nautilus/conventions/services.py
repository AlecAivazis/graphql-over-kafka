"""
    This file is responsible for centralizing the service conventions used in nautilus.
"""

# local imports
from .models import get_model_string, normalize_string

def model_service_name(model):
    ''' the name of a service that manages a model '''
    return get_model_string(model)


def auth_service_name():
    return "auth"


def api_gateway_name():
    ''' the name of the default api gateway '''
    return "api"


def connection_service_name(service, *args):
    ''' the name of a service that manages the connection between services '''
    # if the service is a string
    if isinstance(service, str):
        return service

    return normalize_string(type(service).__name__)
