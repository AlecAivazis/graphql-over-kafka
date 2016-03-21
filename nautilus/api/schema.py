# external imports
from graphene import Schema
# local imports
from .executor import TornadoExecutor

class NautilusSchema(Schema):
    """
        This class creates a graphql schema that resolves its fields using
        the natuilus event queue for asynchronous data retrieval.
    """
    def __init__(self, **kwds):
        # make sure the schema is built with a tornado executor
        super().__init__(executor=TornadoExecutor(), **kwds)
