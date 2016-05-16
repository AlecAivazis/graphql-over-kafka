import json
import tornado.gen
from tornado.web import MissingArgumentError
from graphql.error import format_error as format_graphql_error
# local imports
from nautilus.auth import AuthRequestHandler


class GraphQLRequestHandler(AuthRequestHandler):

    def initialize(self, schema=None):
        self._schema = schema

    @property
    def request_context(self):
        return self

    @tornado.web.asynchronous
    def get(self):
        try:
            # grab the query from the request parameters
            query = self.get_query_argument('query')

            # log the request
            print("handling graphql query: {}".format(query))

            # execute the query
            result = self._schema.execute(
                query,
                context_value=self.request_context
            )
            print(result)

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
            self.finish(json.dumps(result_dict))

        # if the user forgot to specify a query
        except MissingArgumentError:
            # return a graphql response with the error
            return self.finish(json.dumps({
                'errors': ['No query given.']
            }))


    # TODO: generalize this
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        try:
            # grab the query from the request parameters
            query = json.loads(self.request.body.decode('utf-8'))['query']
            # log the request
            print("handling graphql query: {}".format(query))

            # execute the
            result = self._schema.execute(
                query,
                request_context=self.request_context
            )

            # format the errors specially
            errors = [str(format_graphql_error(error)) \
                                            for error in result.errors]

            # create a dictionary version of the result
            result_dict = dict(data=result.data)
            # if there are errors
            if errors:
                # add them to the result
                result_dict['errors'] = ','.join(errors) or []

            # send the response to the client and close its connection
            self.finish(json.dumps(result_dict))

        # if the user forgot to specify a query
        except MissingArgumentError:
            # return a graphql response with the error
            return self.finish(json.dumps({
                'errors': ['No query given.']
            }))
