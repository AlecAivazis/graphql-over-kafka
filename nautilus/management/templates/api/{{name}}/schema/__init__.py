# external imports
from graphene import Schema
# local imports
from .query import Query


# create the schema based on the query object
schema = Schema(name='My Schema', auto_camelcase=False)
schema.query = Query
