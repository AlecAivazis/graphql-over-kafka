# local imports
from .graphql import GraphQLRequestHandler

class APIQueryHandler(GraphQLRequestHandler):
    """
        This request handler add slight modifications to the logic
        in order to support external acces.
    """