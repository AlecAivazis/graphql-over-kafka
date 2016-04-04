# external imports
import graphene
from graphene import Field, List
# local imports
from .filter import args_for_model, filter_model
from nautilus.contrib.graphene_peewee import PeeweeObjectType, convert_peewee_field


def create_model_schema(Model):
    """ This function creates a graphql schema that provides a single model """

    from nautilus.database import db

    # create the schema instance
    schema = graphene.Schema(auto_camelcase = False)

    # grab the primary key from the Model
    primary_key = Model.primary_key()
    primary_key_type = convert_peewee_field(primary_key)

    # create a graphene object
    class ModelObjectType(PeeweeObjectType):
        class Meta:
            model = Model

        primary_key = Field(primary_key_type, description = "The primary key for this object.")


        def resolve_primary_key(self, args, info):
            return self.primary_key


    class Query(graphene.ObjectType):
        """ the root level query """
        all_models = List(ModelObjectType, args=args_for_model(Model))

        def resolve_all_models(self, args, info):
            # filter the model query according to the arguments
            return filter_model(Model, args)


    # add the query to the schema
    schema.query = Query

    return schema
