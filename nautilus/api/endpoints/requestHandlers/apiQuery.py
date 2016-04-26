# local imports
from .graphql import GraphQLRequestHandler

class APIQueryHandler(GraphQLRequestHandler):
    """
        This request handler add slight modifications to the logic
        in order to support external acces.
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods"," GET, POST, OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", True)
        self.set_header("Access-Control-Allow-Headers"," accept, content-type")
