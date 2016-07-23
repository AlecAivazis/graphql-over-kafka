# external imports
import graphene
from graphene import ObjectType, Field, List
# local imports
from .graphql_type_from_summary import graphql_type_from_summary
from .graphql_mutation_from_summary import graphql_mutation_from_summary

def generate_api_schema(models, connections=[], mutations=[], **schema_args):

    # collect the schema types
    schema_types = []

    # for each model
    for model in models:
        # find any matching connections
        model_connections = [connection for connection in connections \
                    if connection['connection']['from']['service'] == model['name']]
        # build a graphql type for the model
        graphql_type = graphql_type_from_summary(model, model_connections)

        # add the graphql type to the list
        schema_types.append(graphql_type)

    # if there are types for the schema
    if schema_types:
        # create a query with a connection to each model
        query = type('Query', (ObjectType,), {
            field.__name__: List(field) for field in schema_types
        })

        # create mutations for each provided mutation
        mutations = [graphql_mutation_from_summary(mut) for mut in mutations]

        # if there are mutations to add
        if mutations:
            # create an object type to contain the mutations
            mutations = type('Mutations', (ObjectType,), {
                mut._meta.object_name: graphene.Field(mut) for mut in mutations
            })

        # build the schema with the query object
        schema = graphene.Schema(
            query=query,
            mutation=mutations,
            **schema_args
        )

        return schema
