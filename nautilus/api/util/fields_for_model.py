# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

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
    args = {field.name.lower() : convert_peewee_field(field) \
                                        for field in model.fields()}
    # use the field arguments, without the segments
    return args
