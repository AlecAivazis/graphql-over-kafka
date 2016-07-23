# external imports
import graphene
# local imports
from .build_native_type_dictionary import build_native_type_dictionary

def graphql_mutation_from_summary(summary):
    """
        This function returns a graphql mutation corresponding to the provided
        summary.
    """
    # get the name of the mutation from the summary
    mutation_name = summary['name']

    # print(summary)

    # the treat the "type" string as a gra
    input_fields = build_native_type_dictionary(summary['inputs'], respect_required=True)

    # the inputs for the mutation are defined by a class record
    inputs = type('Input', (object,), input_fields)

    # the outputs for the mutation are attributes to the class record
    outputs = build_native_type_dictionary(summary['outputs'], respect_required=False)

    # create the output type

    # create the appropriate mutation class record
    mutation = type(mutation_name, (graphene.Mutation,), {
        'Input': inputs,
        **outputs
    })

    # return the newly created mutation record
    return mutation