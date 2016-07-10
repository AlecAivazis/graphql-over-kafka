# external imports
import graphene
from graphene import Field, List
# local imports
from ..filter import filter_model, args_for_model
from nautilus.contrib.graphene_peewee import PeeweeObjectType, convert_peewee_field


def create_model_schema(target_model):
    """ This function creates a graphql schema that provides a single model """

    from nautilus.database import db

    # create the schema instance
    schema = graphene.Schema(auto_camelcase=False)

    # grab the primary key from the model
    primary_key = target_model.primary_key()
    primary_key_type = convert_peewee_field(primary_key)

    # create a graphene object
    class ModelObjectType(PeeweeObjectType):
        class Meta:
            model = target_model

        pk = Field(primary_key_type, description="The primary key for this object.")

        @graphene.resolve_only_args
        def resolve_pk(self):
            return getattr(self, self.primary_key().name)


    class Query(graphene.ObjectType):
        """ the root level query """
        all_models = List(ModelObjectType, args=args_for_model(target_model))


        @graphene.resolve_only_args
        def resolve_all_models(self, **args):
            # filter the model query according to the arguments
            # print(filter_model(target_model, args)[0].__dict__)
            return filter_model(target_model, args)


    # add the query to the schema
    schema.query = Query

    return schema

