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
            mutation_args = {arg.name.value: arg.value.value for arg in mutation.arguments}
            # the requested fields
            mutation_selections = mutation.selection_set.selections
            # the fields are treated as a list of fields to be passed along
            mutation_fields = [field.name.value for field in mutation_selections]

            # pass the necessary information to the mutation resolver
            try:
                mut_result = await mutation_resolver(
                    mutation_name,
                    mutation_args,
                    mutation_fields
                )

                # if there is only one field and it is an object
                # TODO: clean this up!!!!
                #       support more than just one nested object (see GH for discussion)
                if len(mutation_selections) == 1 and \
                        mutation_selections[0].selection_set and \
                        len(mutation_selections[0].selection_set.selections) > 0:
                    # grab the only mutation field so we can nest appropriately
                    mutations_result[mutation_name] = {
                        mutation_selections[0].name.value: mut_result
                    }
                # otherwise
                else:
                    mutations_result[mutation_name] = mut_result
            # if something goes wrong
            except Exception as e :
                # add the error to the list
                errors.append(str(e))


    # if any mutations were performed
    if mutations_result:
        # add the result to the final summary
        result['mutation'] = mutations_result


    # return the final result
    return {
        'errors': errors,
        **result
    }
