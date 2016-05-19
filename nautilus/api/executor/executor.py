# external imports
import tornado
import tornado.gen
from promise import Promise

class TornadoExecutor:
    """
        This class executes a schema asynchronously using the tornado ioloop.
    """

    def __init__(self, futures={}):
        self.future = None
        self.ioloop = tornado.ioloop.IOLoop.current()

    @tornado.gen.engine
    def _fn_future(self, fn, source, args, context, info):
        return tornado.gen.Task(fn, source, args, context, info)

    @tornado.gen.coroutine
    def wait_until_finished(self):
        # print("waiting....")
        # while True:
        #     # wait for the future to finish
        #     result = yield self.future

        #     if result:
        #         print("result: {}".format(result))
        #         break

        # return result
        # # self.ioloop.add_future(self.future, self.promise.fulfill)
        self.future.set_result('hello')


    def execute(self, resolve_fn, source, args, context, info):
        self.promise = Promise()


        # create the future for the fn
        self.future = self._fn_future(resolve_fn, source, args, context, info)
        # when the future finishes it should resolve its value
        self.future.add_done_callback(lambda future: self.promise.fulfill(future.result()))

        return self.promise