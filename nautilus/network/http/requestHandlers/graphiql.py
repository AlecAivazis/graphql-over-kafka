import tornado.web
import tornado.gen
import tornado.template
import json


class GraphiQLRequestHandler(tornado.web.RequestHandler):

    def initialize(self, schema=None, async=False):
        self._schema = schema
        # TODO: check for async executor in schema
        self._async = async

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        if not self._schema:
            self.finish('no schema!')
            return

        query = '{ hello }'

        # if the schema is synchronously executed
        if not self._async:
            # execute the
            result = self._schema.execute(query)
        # otherwise the schema is asynchronously executed
        else:
            # resolve the schema in a coroutine
            result = yield tornado.gen.Task(self._schema.execute, query)

        # send the response to the client and close its connection
        self.finish(json.dumps(result.data))
