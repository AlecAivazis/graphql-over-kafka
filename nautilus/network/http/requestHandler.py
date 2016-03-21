import tornado
import json


class GraphqlRequestHandler(tornado.web.RequestHandler):

    def initialize(self, schema=None):
        self._schema = schema

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        if not self._schema:
            self.finish('no schema!')
            return

        query = '{ hello, goodbye }'

        # resolve the schema in a coroutine
        result = yield tornado.gen.Task(self._schema.execute, query)
        # send the response to the client and close its connection
        self.finish(json.dumps(result.data))

# class GraphqlRequestHandler(tornado.web.RequestHandler):

#         @tornado.web.asynchronous
#         @tornado.gen.engine
#         def get(self):

#             print("HELLO")
#             self.finish('hello')
