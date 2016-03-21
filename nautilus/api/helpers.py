# external imports
import graphene
from graphene import Field, List
from graphene.contrib.sqlalchemy import SQLAlchemyObjectType
from sqlalchemy.inspection import inspect
# local imports
from nautilus.api.filter import args_for_model, filter_model
from nautilus.api import convert_sqlalchemy_type


def create_model_schema(Model):
    """ This function creates a graphql schema that provides a single model """

    from nautilus.db import db

    # create the schema instance
    schema = graphene.Schema(
        session = db.session,
        auto_camelcase = False
    )

    # grab the primary key from the Model
    primary_key = inspect(Model).primary_key[0]
    primary_key_type = convert_sqlalchemy_type(primary_key.type, primary_key)

    # create a graphene object registered with the schema
    @schema.register
    class ModelObjectType(SQLAlchemyObjectType):
        class Meta:
            model = Model

        primary_key = Field(primary_key_type, description = "The primary key for this object.")


        def resolve_primary_key(self, args, info):
            return self.primary_key()


    class Query(graphene.ObjectType):
        """ the root level query """
        all_models = List(ModelObjectType,
                          args=args_for_model(Model)
                         )

        def resolve_all_models(self, args, info):
            # filter the model query according to the arguments
            return filter_model(Model, args)


    # add the query to the schema
    schema.query = Query

    return schema

