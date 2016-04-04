import json
import tornado.gen
from tornado.web import MissingArgumentError
from graphql.core.error import (
    GraphQLError,
    format_error as format_graphql_error
)
# local imports
from nautilus.network.http import RequestHandler


class GraphQLRequestHandler(RequestHandler):

    def initialize(self, schema=None, async=False):
        self._schema = schema
        # TODO: check for async executor in schema
        self._async = async

    def get_request_context(self):
        return self

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        try:
            # grab the query from the request parameters
            query = self.get_query_argument('query')

            # if the schema is synchronously executed
            if not self._async:
                # execute the
                result = self._schema.execute(
                    query,
                    requres_context=self.get_request_context()
                )
            # otherwise the schema is asynchronously executed
            else:
                # resolve the schema in a coroutine
                result = yield tornado.gen.Task(self._schema.execute, query)

            # format the errors specially
            errors = [str(format_graphql_error(error)) \
                                            for error in result.errors]

            # send the response to the client and close its connection
            self.finish(json.dumps({
                'data': result.data,
                'errors': ','.join(errors) or []
            }))

        # when something goes wrong
        except Exception as err:
            # if the user forgot to specify a query
            if isinstance(err, MissingArgumentError):
                return self.finish(json.dumps({
                    'errors': ['No query given.']
                }))

            # its an exception that isn't our responsibility
            raise err
