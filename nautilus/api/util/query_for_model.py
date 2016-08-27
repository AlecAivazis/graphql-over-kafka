from .arg_string_from_dict import arg_string_from_dict

def query_for_model(fields, **filters):
    # if there are filters
    if filters:
        # the string for the filters
        filter_string = "(%s)" % arg_string_from_dict(filters)
    else:
        filter_string = ''

    # the query for the requested data
    return "query { all_models%s { %s } }" % (filter_string, ', '.join(fields))
