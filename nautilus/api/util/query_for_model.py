def query_for_model(fields, **filters):
    # if there are filters
    if filters:
        # the string for the filters
        filter_string = "(%s)" % ",".join("{}: {}".format(key, json.dumps(value)) for key,value in filters.items())
    else:
        filter_string = ''

    # the query for the requested data
    return """
        query {
            all_models%s {
                %s
            }
        }
    """ % (filter_string, ', '.join(fields))
