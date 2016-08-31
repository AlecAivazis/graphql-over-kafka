"""
    This file is responsible for centralizing the service conventions used in nautilus.
"""

# local imports
from .models import get_model_string, normalize_string

def model_service_name(*models):
    ''' the name of a service that manages a model '''
    return ':'.join([get_model_string(model) for model in models])


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
