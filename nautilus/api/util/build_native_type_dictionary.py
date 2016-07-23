# local imports
from .convert_typestring_to_api_native import convert_typestring_to_api_native
from .graphql_type_from_summary import graphql_type_from_summary

def build_native_type_dictionary(fields, respect_required=False):
    """
        This function takes a list of type summaries and builds a dictionary
        with native representations of each entry. Useful for dynamically
        building native class records from summaries.
    """
    # a place to start when building the input field attributes
    input_fields = {}
    # go over every input in the summary
    for field in fields:

        field_name = field['name']
        field_type = field['type']

        # if the type field is a string
        if isinstance(field_type, str):
            # compute the native api type for the field
            field_type = convert_typestring_to_api_native(field_type)()
            # add an entry in the attributes
            input_fields[field_name] = field_type

        # we could also be looking at a dictionary
        elif isinstance(field_type, dict):

            object_fields = field_type['fields']

            # add the dictionary to the parent as a graphql object type
            input_fields[field_name] = graphql_type_from_summary(
                summary={
                    'name': field_name,
                    'fields': object_fields
                }
            )

    # we're done
    return input_fields
