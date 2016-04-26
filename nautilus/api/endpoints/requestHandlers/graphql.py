import json
import tornado.gen
from tornado.web import MissingArgumentError
from graphql.core.error import format_error as format_graphql_error
# local imports
from nautilus.auth import AuthRequestHandler


class GraphQLRequestHandler(AuthRequestHandler):

    def initialize(self, schema=None, async=False):
        self._schema = schema
        # TODO: check for async executor in schema
        self._async = async

    @property
    def request_context(self):
        return self

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            # grab the query from the request parameters
            query = self.get_query_argument('query')

            # log the request
            print("handling graphql query: {}".format(query))

            # if the schema is synchronously executed
            if not self._async:
                # execute the
                result = self._schema.execute(
                    query,
                    request_context=self.request_context
                )
            # otherwise the schema is asynchronously executed
            else:
                # resolve the schema in a coroutine
                result = yield tornado.gen.Task(self._schema.execute, query)

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


    # TODO: generalize this
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        try:
            # grab the query from the request parameters
            query = json.loads(self.request.body.decode('utf-8'))['query']
            # log the request
            print("handling graphql query: {}".format(query))

            # if the schema is synchronously executed
            if not self._async:
                # execute the
                result = self._schema.execute(
                    query,
                    request_context=self.request_context
                )
            # otherwise the schema is asynchronously executed
            else:
                # resolve the schema in a coroutine
                result = yield tornado.gen.Task(self._schema.execute, query)

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
