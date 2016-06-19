import json
from graphql.error import format_error as format_graphql_error
# local imports
from nautilus.auth import AuthRequestHandler
from nautilus.network.http import Response

class GraphQLRequestHandler(AuthRequestHandler):

    async def get(self):
        try:
            # grab the query from the request parameters
            query = self.request.GET['query']
        # if the user forgot to specify a query
        except KeyError:
            # return a graphql response with the error
            return Response(body=json.dumps({
                'errors': ['No query given.']
            }).enocde())

        # handle the query
        return await self._handle_query(query)

    async def post(self):
        try:                # grab the query from the request parameters
            query = self.request.POST['query']
        # if the user forgot to specify a query
        except KeyError:
            # return a graphql response with the error
            return Response(body=json.dumps({
                'errors': ['No query given.']
            }).enocde())

        # handle the query
        return await self._handle_query(query)


    @property
    def request_context(self):
        return self


    @property
    def schema(self):
        self.__class__.schema


    async def _handle_query(self, query):

        # log the request
        print("handling graphql query: {}".format(query))

        # execute the query
        result = schema.execute(
            query,
            context_value=self.request_context
        )

        # format the errors specially
        errors = [str(error) for error in result.errors]

        # create a dictionary version of the result
        result_dict = dict(data=result.data)
        # if there are errors
        if errors:
            print(result.errors)
            # add them to the result
            result_dict['errors'] = ','.join(errors) or []

        # send the response to the client and close its connection
        return Response(body=json.dumps(result_dict).encode())
