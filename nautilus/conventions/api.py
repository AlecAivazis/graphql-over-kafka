"""
    This file is responsible for centralizing the schema conventions used in nautilus.
"""
# external imports
from functools import singledispatch
from .models import normalize_string, get_model_string
import nautilus

def root_query(*service):
    ''' This function returns the name of the root query for a model service. '''
    return 'all_models'


def crud_mutation_name(action, model):
    """
        This function returns the name of a mutation that performs the specified
        crud action on the given model service
    """
    return "{}_{}".format(action, get_model_string(model))
