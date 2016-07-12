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
            }).encode())

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
            }).encode())

        # handle the query
        return await self._handle_query(query)


    @property
    def request_context(self):
        return self


    @property
    def schema(self):
        return self.service.schema


    @property
    def service(self):
        return self.__class__.service


    async def _handle_query(self, query):

        # log the request
        print("handling graphql query: {}".format(query))

        # execute the query
        result = self.schema.execute(
            query,
            context_value=self.request_context
        )

        # create a dictionary version of the result
        result_dict = dict(
            data=result.data,
            errors= [str(error) for error in result.errors]
        )

        # send the response to the client and close its connection
        return Response(body=json.dumps(result_dict).encode())
