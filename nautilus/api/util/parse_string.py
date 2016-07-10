# external imports
from graphql import parse
# local imports
from .walk_query import walk_query

async def parse_string(query, resolver, connection_resolver):

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
