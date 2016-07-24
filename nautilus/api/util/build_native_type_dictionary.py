# external imports
import graphene
# local imports
from .convert_typestring_to_api_native import convert_typestring_to_api_native
from .graphql_type_from_summary import graphql_type_from_summary

def build_native_type_dictionary(fields, respect_required=False, wrap_field=True, name=''):
    """
        This function takes a list of type summaries and builds a dictionary
        with native representations of each entry. Useful for dynamically
        building native class records from summaries.
    """
    # a place to start when building the input field attributes
    input_fields = {}
    # go over every input in the summary
    for field in fields:
        field_name = name + field['name']
        field_type = field['type']

        # if the type field is a string
        if isinstance(field_type, str):
            # compute the native api type for the field
            field_type = convert_typestring_to_api_native(field_type)(
                # required=respect_required and field['required']
            )
            # add an entry in the attributes
            input_fields[field['name']] = field_type

        # we could also be looking at a dictionary
        elif isinstance(field_type, dict):

            object_fields = field_type['fields']

            # add the dictionary to the parent as a graphql object type
            input_fields[field['name']] = graphql_type_from_summary(
                summary={
                    'name': field_name+"ArgType",
                    'fields': object_fields
                }
            )

            # if we are supposed to wrap the object in a field
            if wrap_field:
                # then wrap the value we just added
                input_fields[field['name']] = graphene.Field(input_fields[field['name']])


    # we're done
    return input_fields
