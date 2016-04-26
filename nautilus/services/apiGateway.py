# local imports
from nautilus.conventions.services import api_gateway_name
from .service import Service
from nautilus.api.endpoints import APIQueryHandler


class APIGateway(Service):
    """
        This provides a single endpoint that other services and clients can
        use to query the cloud without worrying about the distributed nature
        of the system.

        Args:
            schema (graphql.core.type.GraphQLSchema): The schema to use that
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


    @property
    def _api_request_handler_class(self):
        return APIQueryHandler
