# third party imports
from graphene import ObjectType, Schema, List, Field, Int, String
from graphql.core.type import  GraphQLInt, GraphQLString
from graphene.contrib.sqlalchemy import SQLAlchemyObjectType
from nautilus.schema import Connection
# local imports
from .models import Sensor as SensorModel

class Sensor(SQLAlchemyObjectType):
    """ The product of a particular brand """

    class Meta:
        model = SensorModel


class Query(ObjectType):
    """ The root level query """
    sensors = Connection(Sensor)

    def resolve_sensors(self, args, info):
        # retrieve the sensors from the database
        return SensorModel.query.all()


# create the schema based on the query object
schema = Schema(name='Sensor Schema')
schema.query = Query
