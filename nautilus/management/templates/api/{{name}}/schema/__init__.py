# external imports
from graphene import ObjectType, Schema, resolve_only_args, List, String
# local imports
from .query import Query


# create the schema based on the query object
schema = Schema(name='Product Schema', auto_camelcase=False)
schema.query = Query
