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
