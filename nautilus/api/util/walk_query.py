# external imports
from graphql import parse

async def walk_query(obj, object_resolver, connection_resolver, errors, __naut_name=None, **filters):
    """
        This function traverses a query and collects the corresponding
        information in a dictionary.
    """


    # if the object has no selection set
    if not hasattr(obj, 'selection_set'):
        # yell loudly
        raise ValueError("Can only resolve objects, not primitive types")

    # the name of the node
    node_name = __naut_name or obj.name.value if obj.name else obj.operation

    # the selected fields
    selection_set = obj.selection_set.selections

    # the fields we have to ask for
    fields = [field for field in selection_set if not field.selection_set]
    # the links between objects
    connections = [field for field in selection_set if field.selection_set]

    try:
        # resolve the model with the given fields
        models = await object_resolver(node_name, [field.name.value for field in fields], **filters)
    # if something went wrong resolving the object
    except Exception as e:
        # add the error as a string
        errors.append(e.__str__())
        # stop here
        return None

    # print(models)
    # add connections to each matching model
    for model in models:
        # if is an id for the model
        if 'pk' in model:
            # for each connection
            for connection in connections:
                # the name of the connection
                connection_name = connection.name.value
                # the target of the connection
                node = {
                    'name': node_name,
                    'pk': model['pk']
                }

                try:
                    # go through the connection
                    connected_ids, next_target = await connection_resolver(
                        connection_name,
                        node,
                    )

                    # if there are connections
                    if connected_ids:
                        # add the id filter to the list
                        filters['pk_in'] = connected_ids

                        # add the connection field
                        value = await walk_query(
                            connection,
                            object_resolver,
                            connection_resolver,
                            errors,
                            __naut_name=next_target,
                            **filters
                        )
                    # there were no connections
                    else:
                        value = []
                # if something went wrong
                except Exception as e:
                    # add the error as a string
                    errors.append(e.__str__())
                    # stop here
                    value = None

                # set the connection to the appropriate value
                model[connection_name] = value

    # return the list of matching models
    return models


async def resolve_string(query, resolver, connection_resolver):

    # parse the query
    query_parsed = parse(query)

    # the query operations contained in the string
    queries = [operation for operation in query_parsed.definitions \
                                    if operation.operation == 'query']

    # TODO: handle multiple queries per string
    # grab the first query with no name
    query = [query for query in queries if not query.name][0]

    # start off with an empty dictionary
    result = {}
    # collect the errors in a list
    errors = []

    # go to each selection set of the query
    for selection in query.selection_set.selections:
        # walk the selection and add it to the result
        result[selection.name.value] = await walk_query(selection, resolver, connection_resolver, errors)


    # return the final result
    return {
        'data': result,
        'errors': errors
    }
