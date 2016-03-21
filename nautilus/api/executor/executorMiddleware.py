import uuid
import tornado
import time
from tornado.concurrent import Future
from graphql.core.pyutils.defer import Deferred
from graphql.core.execution.middlewares.utils import resolver_has_tag, tag_resolver


_nautilus_tag = 'nautilus_service'

def nautilus_service(f):
    """
        Marks a resolver to run inside the ioloop.
    """
    return tag_resolver(f, _nautilus_tag)

@tornado.gen.coroutine
def execute_resolver(resolver, deffered):
    """
        This function executes the given resolver, passing it
    """

    resolver(deferred)


class TornadoExecutionMiddleware:
    """
        This middleware executes the fields using the tornado ioloop for
        deffered executions.
    """

    @staticmethod
    def run_resolve_fn(resolver, original_resolver):
        """
            This method acts as a wrapper over the fields resolve function.
            In order to integrate seemlessly with graphql.core, the result
            is wrapped in <graphql.core.pyutils.Deferred> when necessary.
        """
        # if the field is an asynchronous one
        if resolver_has_tag(original_resolver, _nautilus_tag):
            # create a deffered object
            deferred = Deferred()
            # execute the resolver and hand it the deferred so it can use the
            # callback
            execute_resolver(resolver, deferred)
            # return the deferred object
            return deferred

        # otherwise the field should be executed synchrnously
        return resolver()


    @staticmethod
    def execution_result(executor):
        """
            This method waits for the deffered execution. Unfortunately,
            this method is not forced asynchronous so we have wrap the
            execution in a future.
        """
        # create a tornado future
        future = Future()

        # retrieve the deffered execution
        deferred = executor()

        # make sure it is a deffered object
        assert isinstance(deferred, Deferred), (
            'Another middleware has converted the execution result ' + \
                                               'away from a Deferred.'
        )

        # when the deferred is finished update the future
        deferred.add_callbacks(future.set_result, future.set_exception)

        # wait for the result of the async action
        return future
