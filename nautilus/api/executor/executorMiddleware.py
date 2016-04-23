# external imports
import tornado
from tornado.concurrent import Future
from graphql.core.pyutils.defer import Deferred
from graphql.core.execution.middlewares.utils import (
    resolver_has_tag, 
    tag_resolver
)


_async_tag = 'async_field'


def async_field(func):
    """
        Marks a resolver to run inside the ioloop.
    """
    def resolver(self, args, info):

        return func

    return tag_resolver(resolver, _async_tag)


def is_async_field(func):
    """
        This funtion checks if a resolver has the correct tag to designate
        an async field.
    """
    return resolver_has_tag(func, _async_tag)


@tornado.gen.coroutine
def execute_async_resolver(resolver, deferred):
    """
        This function executes the given resolver, passing it
    """
    resolver()(deferred.callback, deferred.errback)


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
        if resolver_has_tag(original_resolver, _async_tag):
            # create a deffered object
            deferred = Deferred()
            # execute the resolver and hand it the deferred so it can use the
            # callback
            execute_async_resolver(resolver, deferred)
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

        # if the executor is not a deffered
        if not isinstance(deferred, Deferred):
            # yell loudly
            raise ValueError('Another middleware has converted the ' +
                             'execution result away from a Deferred.'
                            )

        # when the deferred is finished update the future
        deferred.add_callbacks(future.set_result, future.set_exception)

        # wait for the result of the async action
        return future
