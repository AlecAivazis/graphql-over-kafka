"""
    This file is responsible for centralizing the schema conventions used in nautilus.
"""

def root_query_for_model_service(service):
    ''' This function returns the name of the root query for a model service. '''
    return 'allModels'

def root_query_for_connection_service(service):
    ''' This function returns the name of the root query for a connection service. '''
    return 'connections'
