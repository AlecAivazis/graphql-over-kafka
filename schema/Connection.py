# third party imports
from graphene import Field, List

def Connection(target, **args):
    """ a wrapper for a field that is the connection between two objects """
    return Field( List(target), **args )
