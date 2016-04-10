# external imports
import graphene
from graphene import Field, List
# local imports
from .filter import filter_model, args_for_model
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


def fields_for_model(model):
    """
        This function returns the fields for a schema that matches the provided
        nautilus model.

        Args:
            model (nautilus.model.BaseModel): The model to base the field list on

        Returns:
            (dict<field_name: str, graphqlType>): A mapping of field names to
                graphql types
    """

    # the attribute arguments (no filters)
    args = { field.name.lower() : convert_peewee_field(field) \
                                        for field in model.fields() }

    # add the primary key field

    # the primary keys for the Model
    primary_key = model.primary_key()
    # add the primary key filter to the arg dictionary
    args['pk'] = convert_peewee_field(primary_key)

    # use the field arguments, without the segments
    return args
