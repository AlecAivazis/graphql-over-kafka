"""
    This file describes the GraphQL schema that other services will use to query the inner state
    of this service. For more information on graphql please visit:
        https://facebook.github.io/react/blog/2015/05/01/graphql-introduction.html
"""

# third party imports
from graphene import ObjectType, Schema, List, Field, Int, String
from graphql.core.type import  GraphQLInt, GraphQLString
from graphene.contrib.sqlalchemy import SQLAlchemyObjectType
from nautilus.schema import Connection
# local imports
from .models import Recipe as RecipeModel

class Recipe(SQLAlchemyObjectType):
    """ The product of a particular brand """

    class Meta:
        model = RecipeModel


class Query(ObjectType):
    """ The root level query """
    recipes = Connection(Recipe)

    def resolve_recipes(self, args, info):
        # retrieve the sensors from the database
        return RecipeModel.query.all()


# create the schema based on the query object
schema = Schema(name='Recipe List Schema')
schema.query = Query
