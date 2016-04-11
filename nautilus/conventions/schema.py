"""
    This file is responsible for centralizing the schema conventions used in nautilus.
"""

def root_query(*service):
    ''' This function returns the name of the root query for a model service. '''
    return 'all_models'
