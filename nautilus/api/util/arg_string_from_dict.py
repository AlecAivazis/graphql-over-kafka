import json

def arg_string_from_dict(arg_dict, **kwds):
    """
        This function takes a series of ditionaries and creates an argument
        string for a graphql query
    """
    # the filters dictionary
    filters = {
        **arg_dict,
        **kwds,
    }
    # return the correctly formed string
    return ", ".join("{}: {}".format(key, json.dumps(value)) for key,value in filters.items())