# external imports
import aiohttp_cors
# local imports
import nautilus.api.endpoints.requestHandlers.apiQuery as api_query
import nautilus.network.events.consumers.api as api_handler
from nautilus.conventions.services import api_gateway_name
from nautilus.conventions.actions import roll_call_type
from nautilus.api.endpoints import static_dir as api_endpoint_static
from .service import Service
from nautilus.api.endpoints import (
    GraphiQLRequestHandler,
    GraphQLRequestHandler
)


class APIGateway(Service):
    """
        This provides a single endpoint that other services and clients can
        use to query the cloud without worrying about the distributed nature
        of the system.

        Args:
            schema (graphql.type.GraphQLSchema): The schema to use that
                encapsultes the overall topology of the cloud.

            action_handler (optional, function): The callback function fired
                when an action is recieved. If None, the service does not
                connect to the action queue.

        Example:

            .. code-block:: python

                # external imports
                import nautilus

                # local imports
                from .schema import schema

                class MyAPIGateway(nautilus.APIGateway):
                    schema = schema
    """
    name = api_gateway_name()
    api_request_handler_class = api_query.APIQueryHandler
    action_handler = api_handler.APIActionHandler

    def __init__(self, *args, **kwds):
        # bubble up
        super().__init__(*args, **kwds)
        # attach this service to the action handler
        self.action_handler.service = self


    # when its time for the service to announce itself
    async def announce(self):
        # bubble up
        await super().announce()
        # ask for rollcall aswell
        await self.event_broker.send(
            action_type=roll_call_type(),
            payload='please report yourself'
        )
        # print('sent ' + roll_call_type())


    def init_routes(self):
        # add the cors handler
        self.cors = aiohttp_cors.setup(self.app)

        # for each route that was registered
        for route in self._routes:
            # add the corresponding http endpoint
            self.add_http_endpoint(**route)

        # add the schema reference to graphql handler
        self.api_request_handler_class.service = self

        # add a cors resource
        api_resource = self.cors.add(self.app.router.add_resource("/"))
        # add the root api handler
        self.cors.add(
            api_resource.add_route("GET", self.api_request_handler_class),
            {
                "": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers=("X-Custom-Server-Header",),
                    allow_headers=("X-Requested-With", "Content-Type"),
                    max_age=3600,
                )
            }
        )
        # add the static file urls
        self.app.router.add_static('/graphiql/static/', api_endpoint_static)
        # add the graphiql endpoint
        self.add_http_endpoint('/graphiql', GraphiQLRequestHandler)
