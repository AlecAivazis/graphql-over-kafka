# external imports
from graphql import parse
# local imports
from .walk_query import walk_query

async def parse_string(query, resolver, connection_resolver, mutation_resolver):
    # start off with an empty dictionary
    result = {}
    # collect the errors in a list
    errors = []

    # parse the query
    query_parsed = parse(query)

    # the query operations contained in the string
    queries = [operation for operation in query_parsed.definitions \
                                    if operation.operation == 'query']
    # if there are queries to run
    if queries:
        # start off with an empty dictionary
        query_result = {}

        # TODO: handle multiple queries per string
        # grab the first query with no name
        query = [query for query in queries if not query.name][0]


        # go to each selection set of the query
        for selection in query.selection_set.selections:
            # walk the selection and add it to the result
            query_result[selection.name.value] = await walk_query(selection, resolver, connection_resolver, mutation_resolver, errors)

        # add the query result to the final result
        result['data'] = query_result

    # the mutations contained in the query
    mutations = [operation for operation in query_parsed.definitions
                                    if operation.operation == 'mutation']

    # store the result of all mutations
    mutations_result = {}
    # we need to execute each mutation within each mutation operation
    for mutation_set in mutations:
        for mutation in mutation_set.selection_set.selections:
            # the name of the mutation
            mutation_name = mutation.name.value
            # the args of the query
            mutation_args = {}
            # the requested fields
            mutation_fields = [field.name.value for field in mutation.selection_set.selections]

            # pass the necessary information to the mutation resolver
            mutations_result[mutation_name] = await mutation_resolver(
                mutation_name,
                mutation_args,
                mutation_fields
            )


    # if any mutations were performed
    if mutations_result:
        # add the result to the final summary
        result['mutation'] = mutations_result


    # return the final result
    return {
        'errors': errors,
        **result
    }
