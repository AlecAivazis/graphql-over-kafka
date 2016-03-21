# external imports
import tornado
from graphql.core.execution import Executor
# local imports
from .executorMiddleware import TornadoExecutionMiddleware

class TornadoExecutor(Executor):
    """
        This class executes a schema asynchronously using the tornado ioloop.
    """

    def __init__(self):
        super().__init__([TornadoExecutionMiddleware])

    @tornado.gen.coroutine
    def execute(self, **kwds):
        # perform the normal execution
        future = super().execute(**kwds)
        # since the normal execution returns a tornado future
        # we have to pull the value out before we can use it
        result = yield future
        # return the extracted value
        return result
