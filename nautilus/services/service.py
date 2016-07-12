# external imports
import asyncio
import uvloop
import jinja2
import json
import aiohttp.web
import aiohttp_jinja2
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
# local imports
from nautilus.api.endpoints import static_dir as api_endpoint_static
from nautilus.config import Config
from nautilus.network.events.actionHandlers import roll_call_handler
from nautilus.network.events.consumers import ActionHandler
from nautilus.api.endpoints import (
    GraphiQLRequestHandler,
    GraphQLRequestHandler
)
from nautilus.conventions.actions import intialize_service_action

# enable uvloop for increased performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class ServiceMetaClass(type):
    def __init__(cls, name, bases, attributes):
        from nautilus.conventions.models import normalize_string

        # create the super class
        super().__init__(name, bases, attributes)

        # the base service strings
        base_strings = [normalize_string(name) for name in [
            'service',
            'modelService',
            'ConnectionService'
        ]]

        # if the object does not yet have a name
        if not cls.name or cls.name in base_strings:
            # use the name of the class record
            cls.name = normalize_string(name)

class ServiceActionHandler(ActionHandler):

    async def handle_action(self, action_type, payload, **kwds):
        """
            The default action Handler has no action.
        """
        # if there is a service attached to the action handler
        if hasattr(self, 'service'):
            # handle roll calls
            await roll_call_handler(self.service, action_type, payload, **kwds)


class Service(metaclass=ServiceMetaClass):
    """
        This is the base class for all services that are part of a nautilus
        cloud. This class provides basic functionalities such as registration,
        responding to actions, and predictable api endpoints.

        Args:

            action_handler (optional, function): The callback function fired when
                an action is recieved. If None, the service does not connect to the
                action queue.

            config (optional, class): A python class to use for configuring the
                service.

            name (string): The name of the service. This will be used to
                register the service with the registry as act as the designator
                for a ServiceObjectType.

            schema (optional, graphql.core.type.GraphQLSchema): The GraphQL schema
                which acts as a basis for the external API. If None, no endpoints are
                added to the service.

        Example:

            .. code-block:: python

                import nautilus
                from nautilus.api.util import create_model_schema
                from nautilus.network import crud_handler
                import nautilus.models as models

                class Model(models.BaseModel):
                    name = models.fields.CharField()

                class MyService(nautilus.Service):
                    name = 'My Awesome Service'
                    schema = create_model_schema(Model)
                    action_handler = crud_handler(Model)
    """

    config = None
    name = None
    schema = None
    action_handler = ServiceActionHandler
    api_request_handler_class = GraphQLRequestHandler


    _routes = []

    def __init__(
            self,
            name=None,
            schema=None,
            action_handler=None,
            config=None,
            auth=True,
    ):

        self.name = name or self.name or type(self).name
        self.app = None
        self.__name__ = self.name
        self.event_broker = None
        self.schema = schema or self.schema

        # wrap the given configuration in the nautilus wrapper
        self.config = Config(self.config, config)

        # initialize the service
        self.init_app()
        self.init_routes()
        self.init_action_handler()

        # placeholders
        self._http_server = None
        self._server_handler = None

        # cleanup


    def init_app(self):
        from nautilus.api.endpoints import template_dir as api_template_dir
        from nautilus.auth import template_dir as auth_template_dir
        # the secret key
        secret_key = 'NERbTdtQl7IrBM9kx1PDjJXiyZhWWBZ9E7q2B3U7KVE='
        # create a web application instance
        self.app = aiohttp.web.Application(
            middlewares=[
                session_middleware(
                    EncryptedCookieStorage(secret_key)
                )
            ]
        )
        # add the template loader
        aiohttp_jinja2.setup(self.app,
            loader=jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(api_template_dir),
                jinja2.FileSystemLoader(auth_template_dir)
            ])
        )
        # TODO:
            # debug mode

        # attach the ioloop to the application
        self.loop = asyncio.get_event_loop()
        # attach the service to the loop
        self.loop.service = self


    async def announce(self):
        """
            This method is used to announce the existence of the service
        """
        # send a serialized event
        await self.event_broker.send(
            action_type=intialize_service_action(),
            payload=json.dumps(self.summarize())
        )


    def summarize(self, **extra_fields):
        # return the summary
        return dict(name=str(self.name), **extra_fields)


    def init_routes(self):
        # for each route that was registered
        for route in self._routes:
            # add the corresponding http endpoint
            self.add_http_endpoint(**route)

        # add the schema reference to graphql handler
        self.api_request_handler_class.service = self

        # add the static file urls
        self.app.router.add_static('/graphiql/static/', api_endpoint_static)
        # add the default api  handler
        self.add_http_endpoint('/', self.api_request_handler_class)
        # add the graphiql endpoint
        self.add_http_endpoint('/graphiql', GraphiQLRequestHandler)


    def init_action_handler(self):
        # if the service was provided an action handler
        if self.action_handler:
            # create a wrapper for it
            self.event_broker = self.action_handler()
            # pass the service to the event broker
            self.event_broker.service = self


    def run(self, host="localhost", port=8000, shutdown_timeout=60.0, **kwargs):
        """
            This function starts the service's network intefaces.

            Args:
                port (int): The port for the http server.
        """
        print("Running service on http://localhost:%i. " % port + \
                                            "Press Ctrl+C to terminate.")

        # apply the configuration to the service config
        self.config.port = port
        self.config.host = host

        # start the loop
        try:
            # if an event broker has been created for this service
            if self.event_broker:
                # start the broker
                self.event_broker.start()
                # announce the service
                self.loop.run_until_complete(self.announce())

            # the handler for the http server
            http_handler = self.app.make_handler()
            # create an asyncio server
            self._http_server = self.loop.create_server(http_handler, host, port)

            # grab the handler for the server callback
            self._server_handler = self.loop.run_until_complete(self._http_server)
            # start the event loop
            self.loop.run_forever()

        # if the user interrupted the server
        except KeyboardInterrupt:
            # keep going
            pass

        # when we're done
        finally:
            try:
                # clean up the service
                self.cleanup()
            # if we end up closing before any variables get assigned
            except UnboundLocalError:
                # just ignore it (there was nothing to close)
                pass

            # close the event loop
            self.loop.close()


    def cleanup(self):
        """
            This function is called when the service has finished running
            regardless of intentionally or not.
        """

        # if an event broker has been created for this service
        if self.event_broker:
            # stop the event broker
            self.event_broker.stop()
        # attempt
        try:
            # close the http server
            self._server_handler.close()
            self.loop.run_until_complete(self._server_handler.wait_closed())
            self.loop.run_until_complete(self._http_handler.finish_connections(shutdown_timeout))

        # if there was no handler
        except AttributeError:
            # keep going
            pass

        # more cleanup
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.app.cleanup())


    def add_http_endpoint(self, url, request_handler):
        """
            This method provides a programatic way of added invidual routes
            to the http server.

            Args:
                url (str): the url to be handled by the request_handler
                request_handler (nautilus.network.RequestHandler): The request handler
        """
        self.app.router.add_route('*', url, request_handler)


    @classmethod
    def route(cls, route, config=None):
        """
            This method provides a decorator for adding endpoints to the
            http server.

            Args:
                route (str): The url to be handled by the RequestHandled
                config (dict): Configuration for the request handler

            Example:

                .. code-block:: python

                    import nautilus
                    from nauilus.network.http import RequestHandler

                    class MyService(nautilus.Service):
                        # ...

                    @MyService.route('/')
                    class HelloWorld(RequestHandler):
                        def get(self):
                            return self.finish('hello world')
        """
        def decorator(wrapped_class, **kwds):
            # add the endpoint at the given route
            cls._routes.append(
                dict(url=route, request_handler=wrapped_class)
            )
            # return the class undecorated
            return wrapped_class

        # return the decorator
        return decorator


    def _json(self):
        # return a summary of the service
        return self.summarize()

