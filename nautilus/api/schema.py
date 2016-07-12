# external imports
from graphene import Schema

class Schema(Schema):
    """
        This class creates a graphql schema that resolves its fields using
        the natuilus event queue for asynchronous data retrieval.
    """
    def __init__(self, executor=None, auto_camelcase=None, **kwds):
        super().__init__(
            auto_camelcase=False,
            **kwds
        )
