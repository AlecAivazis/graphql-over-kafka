"""
    This file is responsible for centralizing the schema conventions used in nautilus.
"""
# external imports
from functools import singledispatch
from .models import normalize_string
import nautilus

def root_query(*service):
    ''' This function returns the name of the root query for a model service. '''
    return 'all_models'

def service_node_name(service):
    """ This function returns the name of the api node that represents the service """
    # just use the service name
    return normalize_string(service.name)

def model_service_node_name(service):
    return normalize_string(service.name)

def connection_service_node_name(service):
    return normalize_string(service.name)

def service_type_name(service_string):
    return normalize_string(service_string)