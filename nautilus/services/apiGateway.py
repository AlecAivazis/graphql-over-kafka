# local imports
from nautilus.conventions.services import api_gateway_name
from nautilus.network.amqp.actionHandlers import noop_handler
from .service import Service

class APIGatewayMeta(type(Service)):
    def __init__(self, name, bases, attributes):
        # create the super class
        super().__init__(name, bases, attributes)
        # the default name for this class is conventional
        self.name = api_gateway_name()

class APIGateway(Service, metaclass=APIGatewayMeta):
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
