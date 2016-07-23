def convert_typestring_to_api_native(typestring):
    """
        This function converts the typestring representation of an api type to
        the appropriate graphql object.
    """
    import graphene
    return getattr(graphene, typestring)